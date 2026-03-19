# -------------------------------------------------------------------
# CREDENCIALES DE BASE DE DATOS
# -------------------------------------------------------------------
# OJO: esto es solo para local/desarrollo.
# En serio, en cuanto pueda lo paso a variables de entorno (.env)
# y dejo aquí solo lecturas con os.getenv.
DB_CONFIG = {
    "host": "localhost",
    "database": "prueba1",
    "user": "postgres",
    "password": "",  # TODO: mover a variable de entorno
    "port": "5432",
}
# -------------------------------------------------------------------
# CONFIGURACIÓN DE LINKEDIN
# -------------------------------------------------------------------
SECTORES_LINKEDIN = {
    "SECTOR TECNOLÓGICO": "Tecnología OR Software OR IT OR Ciberseguridad",
    "SECTOR INGENIERÍA": "Ingeniería OR Engineering",
    "SECTOR FINANCIERO Y BANCA": "Finanzas OR Banca OR Banking",
    "SECTOR LEGAL": "Legal OR Abogado OR Jurídico",
    "SECTOR VENTAS": "Ventas OR Comercial OR Sales",
    "SECTOR LOGÍSTICA": "Logística OR Supply Chain OR Almacén",
    "SECTOR SERVICIOS": "Servicios OR Atención al cliente",
    "SECTOR SEGUROS": "Seguros OR Insurance"
}

COUNTRIES = ["Spain"]
PAGES = 5

# DATE_POSTED controla la antigüedad de las ofertas
# Lo dejo configurable para poder ajustar scraping según necesidad
DATE_POSTED = "24h"   # "any", "24h", "week", "month"

# EXPERIENCE_LEVELS permite filtrar por seniority
# Uso los códigos internos de LinkedIn
# Si lo dejo vacío, no filtro nada
EXPERIENCE_LEVELS = []  # [] all, ["2"] Entry, ["2","3"] Entry+Associate

# WORKPLACE_TYPES controla si quiero remoto, híbrido o presencial
# Aquí estoy filtrando Remote + Hybrid
WORKPLACE_TYPES = []
SECTORS = []
JOB_KEYWORD = [] # Si este campo es rellenado, se buscará esa palabra clave en el título de la oferta. Si se deja vacío, se buscan todas las ofertas sin filtrar por sectores.

# Configuraciones de rendimiento para el navegador
MAX_SCROLL_ATTEMPTS = 100
SCROLL_PAUSE = 3
DETAIL_PAUSE = 2

# -------------------------------------------------------------------
# TAXONOMÍA DE SECTORES (Para la IA / Clasificador)
# -------------------------------------------------------------------
SECTOR_MAPPING = {
    "118": {
        "subsector": "Computer & Network Security",
        "macro_sector": "Technology",
        "groups": ["tech"],
        "keywords": ["ciberseguridad", "seguridad", "security", "network", "redes", "soc", "siem", "firewall", "hacker", "cybersecurity"]
    },
    "109": {
        "subsector": "Computer Games",
        "macro_sector": "Media & Entertainment",
        "groups": ["tech", "med", "rec"],
        "keywords": ["videojuegos", "games", "gaming", "unity", "unreal", "juego", "gamification"]
    },
    "4": {  # Extra ID para desarrollo de software (común en IT)
        "subsector": "Software Development",
        "macro_sector": "Technology",
        "groups": ["tech"],
        "keywords": ["software", "desarrollo", "programación", "developer", "ingeniero", "frontend", "backend", "fullstack", "react", "python", "java", "net", "c#", "ai", "cloud"]
    },
    "96": { # Extra ID para IT Consulting
        "subsector": "IT Services and IT Consulting",
        "macro_sector": "Technology",
        "groups": ["tech"],
        "keywords": ["it services", "servicios it", "consultoría it", "tecnología de la información", "sistemas", "devops"]
    },

    # --- Healthcare & Pharma ---
    "12": {
        "subsector": "Biotechnology",
        "macro_sector": "Healthcare & Pharma",
        "groups": ["hlth", "tech"],
        "keywords": ["biotecnología", "biotech", "ciencias de la vida", "life sciences", "laboratorio", "investigación", "farmacéutica", "pharma", "medical devices"]
    },
    "125": {
        "subsector": "Alternative Medicine",
        "macro_sector": "Healthcare & Pharma",
        "groups": ["hlth"],
        "keywords": ["medicina alternativa", "terapia", "holístico", "acupuntura", "homeopatía", "naturopatía", "salud", "hospitals"]
    },

    # --- Finance & Insurance ---
    "41": {
        "subsector": "Banking",
        "macro_sector": "Finance & Insurance",
        "groups": ["fin"],
        "keywords": ["banco", "banca", "banking", "financiero", "cajero", "sucursal", "préstamos", "crédito"]
    },
    "47": {
        "subsector": "Accounting",
        "macro_sector": "Finance & Insurance",
        "groups": ["fin", "corp"],
        "keywords": ["contabilidad", "accounting", "contable", "auditoría", "finanzas", "fiscal", "impuestos"]
    },
    "129": {
        "subsector": "Capital Markets",
        "macro_sector": "Finance & Insurance",
        "groups": ["fin"],
        "keywords": ["capital markets", "mercado de capitales", "inversión", "trading", "bolsa", "acciones", "brokers", "wealth management", "venture capital"]
    },

    # --- Manufacturing & Industrial ---
    "53": {
        "subsector": "Automotive",
        "macro_sector": "Manufacturing & Industrial",
        "groups": ["man"],
        "keywords": ["automoción", "vehículos", "coches", "automotive", "motor", "fábrica", "automotriz", "concesionario", "machinery"]
    },
    "54": {
        "subsector": "Chemicals",
        "macro_sector": "Manufacturing & Industrial",
        "groups": ["man"],
        "keywords": ["química", "chemicals", "productos químicos", "planta química", "polímeros", "industrial"]
    },

    # --- Consumer & Retail ---
    "19": {
        "subsector": "Apparel & Fashion",
        "macro_sector": "Consumer & Retail",
        "groups": ["cons", "man"],
        "keywords": ["moda", "ropa", "fashion", "apparel", "textil", "retail", "tienda", "confección", "consumer goods", "ecommerce"]
    },

    # --- Media & Entertainment ---
    "36": {
        "subsector": "Broadcast Media",
        "macro_sector": "Media & Entertainment",
        "groups": ["med"],
        "keywords": ["televisión", "radio", "broadcast", "medios de comunicación", "periodismo", "noticias", "comunicación", "media"]
    },
    "127": {
        "subsector": "Animation",
        "macro_sector": "Media & Entertainment",
        "groups": ["med", "tech"],
        "keywords": ["animación", "3d", "vfx", "motion graphics", "render", "cgi", "producción audiovisual"]
    },
    "111": {
        "subsector": "Arts & Crafts",
        "macro_sector": "Media & Entertainment",
        "groups": ["rec", "man"],
        "keywords": ["arte", "artesanía", "manualidades", "galería", "artista", "pintura", "escultura"]
    },

    # --- Real Estate & Construction ---
    "50": {
        "subsector": "Architecture & Planning",
        "macro_sector": "Real Estate & Construction",
        "groups": ["cons", "tech"],
        "keywords": ["arquitectura", "urbanismo", "architecture", "diseño urbano", "edificación", "arquitecto", "planificación"]
    },
    "49": {
        "subsector": "Building Materials",
        "macro_sector": "Real Estate & Construction",
        "groups": ["cons", "man"],
        "keywords": ["materiales de construcción", "cemento", "ladrillos", "building materials", "cerámica", "hormigón"]
    },
    "51": {
        "subsector": "Civil Engineering",
        "macro_sector": "Real Estate & Construction",
        "groups": ["cons"],
        "keywords": ["ingeniería civil", "obra civil", "infraestructura", "obras", "construcción", "carreteras", "puentes"]
    },
    "128": {
        "subsector": "Commercial Real Estate",
        "macro_sector": "Real Estate & Construction",
        "groups": ["cons", "fin"],
        "keywords": ["bienes raíces", "inmobiliaria", "real estate", "comercial", "propiedades", "alquiler", "locales"]
    },

    # --- Transportation & Logistics ---
    "94": {
        "subsector": "Airlines/Aviation",
        "macro_sector": "Transportation & Logistics",
        "groups": ["tran", "man", "tech"],
        "keywords": ["aerolínea", "aviación", "vuelos", "aviones", "aeropuerto", "piloto", "airlines", "tripulación", "logistics", "shipping"]
    },
    "52": {
        "subsector": "Aviation & Aerospace",
        "macro_sector": "Transportation & Logistics",
        "groups": ["tran", "tech", "man"],
        "keywords": ["aeroespacial", "aerospace", "satélites", "space", "aviónica", "cohetes"]
    },

    # --- Professional Services ---
    "120": {
        "subsector": "Alternative Dispute Resolution",
        "macro_sector": "Professional Services",
        "groups": ["org", "corp"],
        "keywords": ["resolución de conflictos", "mediación", "arbitraje", "disputas", "legal", "abogado", "ley", "derecho"]
    },
    "138": {
        "subsector": "Business Supplies & Equipment",
        "macro_sector": "Professional Services",
        "groups": ["corp", "man"],
        "keywords": ["material de oficina", "equipamiento", "business supplies", "b2b", "proveedores", "consulting", "consultoría empreserial"]
    },

    # --- Government / Civic & Social ---
    "90": {
        "subsector": "Civic & Social Organization",
        "macro_sector": "Government",
        "groups": ["org", "gov"],
        "keywords": ["ong", "organización social", "cívica", "fundación", "non-profit", "voluntariado", "sin ánimo de lucro", "asociación", "public administration", "administración pública", "gobierno"]
    },

    # --- Education ---
    "133": { # Extra ID para Educación
        "subsector": "Higher Education",
        "macro_sector": "Education",
        "groups": ["org"],
        "keywords": ["universidad", "educación", "education", "e-learning", "academia", "formación", "profesor", "colegio", "escuela"]
    },

    # --- Energy & Utilities ---
    "55": { # Extra ID para Energía
        "subsector": "Utilities",
        "macro_sector": "Energy & Utilities",
        "groups": ["man", "cons"],
        "keywords": ["energía", "utilities", "electricidad", "renovables", "solar", "eólica", "oil & gas", "petróleo", "gas", "sostenibilidad"]
    },
}