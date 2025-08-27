import os

# URL de conexión a la base de datos (Supabase para todos los entornos)
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres.jpeibrtqlktbrhwemnbi:Laroca6729@aws-0-sa-east-1.pooler.supabase.com:6543/postgres")

# Debug: Imprimir URL de conexión (sin mostrar password completa)
print(f"🔗 DB URL configured: {SQLALCHEMY_DATABASE_URL[:50]}...")
print(f"🌍 Environment: {os.getenv('ENVIRONMENT', 'not-set')}")



