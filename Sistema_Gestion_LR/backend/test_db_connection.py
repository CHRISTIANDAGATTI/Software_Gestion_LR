"""
Test de conexión a la base de datos para debug
"""
from app.database.session import engine
from sqlalchemy import text

def test_connection():
    try:
        print("🔗 Probando conexión a Supabase...")
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            print("✅ Conexión exitosa!")
            
            # Probar consulta real
            result = connection.execute(text("SELECT COUNT(*) FROM categorias"))
            count = result.fetchone()[0]
            print(f"📊 Categorías en DB: {count}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print(f"🔍 Tipo de error: {type(e)}")

if __name__ == "__main__":
    test_connection()
