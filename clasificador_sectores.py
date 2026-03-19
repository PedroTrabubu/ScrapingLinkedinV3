import re
import config_linkedin as config  # Importo la configuración global (sectores, keywords, etc.)

def clasificar_sector_oferta(job_description, company_description, company_name):
    # Uno toda la información relevante en un único texto para analizarlo de forma conjunta
    # Se pasa todo a minúsculas para evitar problemas de coincidencias
    texto_completo = f"{company_name} {company_description} {job_description}".lower()
    
    # Uso del mapping de sectores definido en el config (ahí está toda la taxonomía)
    taxonomia = config.SECTOR_MAPPING 
    
    # Inicializo un score por cada sector (empiezan todos en 0)
    scores = {sid: 0 for sid in taxonomia}
    
    # Recorro cada sector y sus keywords asociadas
    for sid, info in taxonomia.items():
        for keyword in info.get("keywords", []):
            # Construyo un patrón con bordes de palabra para evitar falsos positivos
            patron = r'\b' + re.escape(keyword.lower()) + r'\b'
            
            # Cuento cuántas veces aparece la keyword en el texto completo
            coincidencias = len(re.findall(patron, texto_completo))
            
            # Si la keyword aparece en nombre o descripción de empresa,
            # le doy más peso porque suele ser más fiable que la descripción del puesto
            peso_empresa = 2 if re.search(patron, f"{company_name} {company_description}".lower()) else 1
            
            # Acumulo score
            scores[sid] += coincidencias * peso_empresa

    # Me quedo con el sector con mayor score
    id_ganador = max(scores, key=scores.get)
    
    # Si ningún sector tiene score (todo 0), lo marco como no clasificado
    if scores[id_ganador] == 0:
        return {
            "id": None,  # En PostgreSQL esto será NULL
            "subsector": "Otro / No clasificado",
            "macro_sector": "Otro / No clasificado",
            "groups": []
        }
        
    # Devuelvo toda la info del sector ganador
    return {
        "id": id_ganador,
        "subsector": taxonomia[id_ganador]["subsector"],
        "macro_sector": taxonomia[id_ganador]["macro_sector"],
        "groups": taxonomia[id_ganador]["groups"]
    }