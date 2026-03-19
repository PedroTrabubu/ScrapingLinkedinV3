import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils_Linkedin import parse_salary

def get_webdriver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument ("--disable-blink-features=AutomationControlled")#LInea nueva Pedro
    #return webdriver.Chrome(options=options)
    driver = webdriver.Chrome(options=options)#LInea nueva Pedro
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")#LInea nueva Pedro
    return driver #LInea nueva Pedro

def scroll_page(driver, max_scrolls, scroll_pause):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0

    while scroll_count < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button, button[aria-label='Ver más empleos'], button[aria-label='See more jobs']")
            for btn in buttons:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(scroll_pause)
                    break
        except Exception:
            pass

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollBy(0, -200);")
            time.sleep(0.5)
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
            if driver.execute_script("return document.body.scrollHeight") == last_height:
                break
        
        last_height = new_height
        scroll_count += 1
    
    print(f"  -> Scroll finalizado ({scroll_count} pasos).")

def fetch_job_details(driver, job_url, detail_pause, max_retries = 2):
    job_desc, company_desc, recruiter_name, recruiter_url = "", "", "", ""
    salary, sector_id, modality = "No especificado", "No especificado", "No especificado"
    exito = False

    for intento in range(max_retries):
        try:
            driver.get(job_url)
            # Si es un reintento, esperamos un poco más para asegurar que carga
            time.sleep(detail_pause + (intento * 3)) 
            #time.sleep(random.uniform(2, 5) + (intento * 3)) #Linea nueva Pedro

            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".description__text, .core-section-container__content, .show-more-less-html__markup"))
            )

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # 1. Salario
            salary_tag = soup.find("div", class_="salary-main-content")
            if salary_tag: salary = salary_tag.get_text(strip=True)

            # 2. Modalidad y Sector
            fit_level_div = soup.find("div", class_="job-details-fit-level-preferences")
            if fit_level_div:
                fit_text = fit_level_div.get_text(strip=True).lower()
                if any(x in fit_text for x in ["remot", "remote", "teletrabajo"]): modality = "Remoto"
                elif any(x in fit_text for x in ["hibrid", "hybrid"]): modality = "Híbrido"
                elif any(x in fit_text for x in ["presencial", "on-site"]): modality = "Presencial"

            criteria_items = soup.find_all("li", class_="description__job-criteria-item")
            for item in criteria_items:
                header = item.find("h3", class_="description__job-criteria-subheader")
                if header:
                    header_text = header.text.strip().lower()
                    val_span = item.find("span", class_="description__job-criteria-text")
                    if val_span:
                        val_text = val_span.get_text(strip=True)
                        if any(x in header_text for x in ["industries", "sector", "industria"]): sector_id = val_text
                        elif any(x in header_text for x in ["workplace", "lugar de trabajo", "modalidad", "lugar", "entorno"]): modality = val_text

            # 3. Descripción
            job_div = soup.find("div", class_="show-more-less-html__markup")
            if not job_div:
                job_div = soup.find("div", class_="description__text")

            if job_div:
                texto_bruto = job_div.get_text(separator="\n", strip=True)
                lineas_limpias = []
                for linea in texto_bruto.split('\n'):
                    linea_baja = linea.lower()
                    if re.search(r'\d+\s*(vacante|solicitante|applicant|candidato)', linea_baja): continue
                    if "hace" in linea_baja and ("día" in linea_baja or "hora" in linea_baja or "semana" in linea_baja): continue
                    lineas_limpias.append(linea)
                    
                job_desc = "\n".join(lineas_limpias).strip()

                if salary == "No especificado":
                    salary_match = re.search(r'(\d{2,3}(?:\.\d{3}|\,\d{3}|k)(?:\s*€|\s*euros)?)', job_desc, re.IGNORECASE)
                    if salary_match: salary = salary_match.group(1)

            if salary != "No especificado": salary = parse_salary(salary)

            # 4. Empresa
            company_div = soup.find("div", class_="show-more-less-html__markup")
            if company_div: company_desc = company_div.get_text(separator="\n", strip=True)

            # 5. Reclutador (Usando exactamente tu código original)
            recruiter_link = soup.find("a", href=lambda x: x and "/in/" in x)
            if recruiter_link:
                recruiter_url = recruiter_link["href"]
                recruiter_name = recruiter_link.get_text(strip=True)

            # Si llegamos a esta línea sin errores, todo salió bien
            exito = True
            break # Salimos del bucle de reintentos

        except Exception as e:
            print(f"      ⚠️ Bloqueo de LinkedIn detectado (Intento {intento+1}/{max_retries}).")
            if intento < max_retries - 1:
                print("      ⏳ Refrescando la página para reintentar...")
                time.sleep(3) # Pausa corta antes de volver a intentar cargar la misma URL

    # FÍJATE AQUÍ: Ahora devolvemos "exito" al final
    return job_desc, company_desc, recruiter_name, recruiter_url, salary, sector_id, modality, exito