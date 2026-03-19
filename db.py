# database.py
import psycopg2
from datetime import datetime, timezone

class Database:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        query = """
        CREATE TABLE IF NOT EXISTS pruebaCondicionalNet (
            id VARCHAR(255) PRIMARY KEY UNIQUE,
            portal VARCHAR(50),
            title VARCHAR(255),
            offer_url TEXT UNIQUE,
            company VARCHAR(255),
            company_url TEXT,
            description TEXT,
            location VARCHAR(255),
            salary_eur VARCHAR(100),
            modality VARCHAR(100),
            publish_date VARCHAR(100),
            sector_name VARCHAR(255),
            recruiter_name VARCHAR(255),
            recruiter_url TEXT,
            taxonomy_id INTEGER,
            taxonomy_subsector VARCHAR(255),
            taxonomy_macro_sector VARCHAR(255),
            taxonomy_groups VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE
        );
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print("   ✅ Base de datos lista: Tabla 'pruebaCondicionalNet' verificada.")
        except Exception as e:
            self.conn.rollback()
            print("   ❌ Error creando la tabla:", e)

    def save_job(self, job):
        try:
            self.cursor.execute(
                """
                INSERT INTO pruebaCondicionalNet
                (id, portal, title, offer_url, company, company_url, description, location, 
                 salary_eur, modality, publish_date, sector_name, recruiter_name, 
                 recruiter_url, taxonomy_id, taxonomy_subsector, taxonomy_macro_sector, 
                 taxonomy_groups, created_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (id) DO UPDATE SET
                    -- Si el salario actual es NULL, lo actualizamos con el nuevo que hemos cazado
                    salary_eur = COALESCE(pruebaCondicionalNet.salary_eur, EXCLUDED.salary_eur),
                    -- (Opcional) Actualizamos también la descripción por si la empresa la modificó
                    description = EXCLUDED.description
                """,
                (
                    job["id"], job["portal"], job["title"], job["offer_url"],
                    job["company"], job["company_url"], job["description"],
                    job["location"], job["salary_eur"], job["modality"],
                    job["publish_date"], job["sector_name"], job.get("recruiter_name", ""),
                    job.get("recruiter_url", ""), job.get("taxonomy_id"),
                    job.get("taxonomy_subsector"), job.get("taxonomy_macro_sector"),
                    job.get("taxonomy_groups"), datetime.now(timezone.utc).isoformat()
                )
            )
            self.conn.commit()
            
            # Comprobamos si ha insertado una nueva o actualizado una existente
            if self.cursor.rowcount > 0:
                print(f"    💾 Guardado/Actualizado: {job['company']} | {job['title']}")
            else:
                print(f"    ⏭️ Ya existía (Sin cambios): {job['title']}")
                
        except Exception as e:
            print(f"\n🚨 ERROR CRÍTICO EN BBDD: {e}")
            self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()