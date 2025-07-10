from app.database.session import SessionLocal
from sqlalchemy import text

def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Conexión a la base de datos exitosa.")
    except Exception as e:
        print("❌ Error de conexión a la base de datos:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_db_connection()
