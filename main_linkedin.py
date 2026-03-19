import time
import re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

from clasificador_sectores import clasificar_sector_oferta
import config_linkedin as config
from db import Database
from utils_Linkedin import build_linkedin_url
from scraperLinkedin import get_webdriver, scroll_page, fetch_job_details


def main():
    db = Database(config.DB_CONFIG)
    driver = get_webdriver()

    # Para evitar duplicados en memoria durante la ejecución
    PROCESSED_JOB_IDS = set()

    contador_ofertas = 0
    errores_consecutivos = 0

    try:
        # Recorremos sectores definidos en config
        for nombre_sector, keyword_busqueda in config.SECTORES_LINKEDIN.items():
            print(f"INICIANDO BÚSQUEDA MASIVA: '{nombre_sector}'")

            for country in config.COUNTRIES:
                print(f"Buscando ofertas en {country}")

                bloques_sin_novedad = 0
                current_start = 0

                # Bucle de paginación
                for p in range(config.PAGES):

                    # Corte por demasiados bloques sin resultados nuevos
                    if bloques_sin_novedad >= 3:
                        if bloques_sin_novedad >= 25:
                            print("Demasiados bloques sin ofertas nuevas. Fin para este sector.")
                        break

                    print(f"\n--- BLOQUE {p+1}/{config.PAGES} | Offset: {current_start} ---")

                    # Aquí se decide si buscar por keyword o por sector
                    if config.JOB_KEYWORD:
                        url = build_linkedin_url(
                            config.JOB_KEYWORD,
                            country,
                            config.EXPERIENCE_LEVELS,
                            config.WORKPLACE_TYPES,
                            config.DATE_POSTED,
                            config.SECTORS,
                            current_start
                        )
                    else:
                        url = build_linkedin_url(
                            keyword_busqueda,
                            country,
                            config.EXPERIENCE_LEVELS,
                            config.WORKPLACE_TYPES,
                            config.DATE_POSTED,
                            config.SECTORS,
                            current_start
                        )

                    # Carga página
                    driver.get(url)
                    time.sleep(config.SCROLL_PAUSE)

                    # Scroll para cargar más ofertas
                    scroll_page(driver, max_scrolls=15, scroll_pause=config.SCROLL_PAUSE)

                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    job_cards = soup.find_all("div", class_="base-card")

                    # Si no hay tarjetas, saltamos más profundo
                    if not job_cards:
                        print("No se encontraron tarjetas. Saltando offset.")
                        current_start += 100
                        bloques_sin_novedad += 1
                        continue

                    print(f"Detectadas {len(job_cards)} ofertas")

                    new_in_block = 0

                    for card in job_cards:
                        urn_tag = card.get("data-entity-urn")
                        job_id = urn_tag.split(":")[-1] if urn_tag else "0"

                        # Evitar duplicados
                        if job_id in PROCESSED_JOB_IDS:
                            continue
                        PROCESSED_JOB_IDS.add(job_id)

                        a_tag = card.find("a", class_="base-card__full-link")
                        job_url = a_tag["href"].split("?")[0].strip() if a_tag else ""
                        if not job_url:
                            continue

                        job_title = (
                            a_tag.find("span", class_="sr-only").text.strip()
                            if a_tag and a_tag.find("span", class_="sr-only")
                            else "Título no encontrado"
                        )

                        contador_ofertas += 1
                        print(f"[{contador_ofertas}] {job_title}")

                        company_tag = card.find("h4", class_="base-search-card__subtitle")
                        company_name = (
                            company_tag.find("a").text.strip()
                            if company_tag and company_tag.find("a")
                            else ""
                        )

                        location_tag = card.find("span", class_="job-search-card__location")
                        location = location_tag.text.strip() if location_tag else ""

                        time_tag = card.find("time", class_="job-search-card__listdate") \
                                   or card.find("time", class_="job-search-card__listdate--new")

                        publish_date = time_tag["datetime"] if time_tag and "datetime" in time_tag.attrs else ""

                        # Filtrado de antigüedad (máx 14 días)
                        if publish_date:
                            try:
                                p_date = datetime.fromisoformat(publish_date)
                                if p_date.tzinfo is None:
                                    p_date = p_date.replace(tzinfo=timezone.utc)

                                diff_days = (datetime.now(timezone.utc) - p_date).days

                                if diff_days > 14:
                                    print(f"Omitiendo oferta antigua ({diff_days} días)")
                                    continue
                            except Exception:
                                pass

                        # Entramos al detalle
                        job_desc, company_desc, recruiter_name, recruiter_url, salary, sector_text, modality, exito = fetch_job_details(
                            driver, job_url, config.DETAIL_PAUSE
                        )

                        # Anti bloqueo
                        if not exito:
                            errores_consecutivos += 1
                            if errores_consecutivos >= 3:
                                print("Posible bloqueo de LinkedIn. Pausa 3 minutos.")
                                time.sleep(180)
                                errores_consecutivos = 0
                        else:
                            errores_consecutivos = 0

                        # Detección de modalidad
                        texto_total = f"{modality} {location} {job_title} {job_desc}".lower()

                        if re.search(r'\b(remoto|remote|teletrabajo)\b', texto_total):
                            modality = "Remoto"
                        elif re.search(r'\b(h[ií]brido|hybrid)\b', texto_total):
                            modality = "Híbrido"
                        elif re.search(r'\b(presencial|on-site|onsite)\b', texto_total):
                            modality = "Presencial"
                        else:
                            modality = "No especificado"

                        # Clasificación sectorial
                        taxonomia = clasificar_sector_oferta(job_desc, company_desc, company_name)

                        # Procesado de salario
                        salario_final = None
                        if salary not in ["No especificado", None, ""]:
                            numeros = re.findall(r'\d+', str(salary))
                            if len(numeros) >= 2:
                                salario_final = f"{numeros[0]} - {numeros[1]}"
                            elif len(numeros) == 1:
                                salario_final = numeros[0]

                        # Construcción del objeto final
                        job_data = {
                            "id": job_id,
                            "portal": "LinkedIn",
                            "title": job_title,
                            "offer_url": job_url,
                            "company": company_name,
                            "company_url": (
                                company_tag.find("a")["href"].split("?")[0]
                                if company_tag and company_tag.find("a")
                                else ""
                            ),
                            "description": job_desc,
                            "location": location,
                            "salary_eur": salario_final,
                            "modality": modality,
                            "publish_date": publish_date,
                            "sector_name": nombre_sector,
                            "recruiter_name": recruiter_name,
                            "recruiter_url": recruiter_url,
                            "taxonomy_id": taxonomia["id"],
                            "taxonomy_subsector": taxonomia["subsector"],
                            "taxonomy_macro_sector": taxonomia["macro_sector"],
                            "taxonomy_groups": ", ".join(taxonomia.get("groups", [])),
                        }

                        db.save_job(job_data)
                        new_in_block += 1

                    # Control de avance de paginación
                    if new_in_block == 0:
                        bloques_sin_novedad += 1
                        current_start += 100
                    else:
                        bloques_sin_novedad = 0
                        current_start += 50

        print(f"\nScraping finalizado. Total ofertas únicas: {len(PROCESSED_JOB_IDS)}")

    except Exception:
        import traceback
        print("ERROR CRÍTICO")
        traceback.print_exc()
        input("Presiona ENTER para salir")

    finally:
        driver.quit()
        db.close()


if __name__ == "__main__":
    main()