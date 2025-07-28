import os

# URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres.jpeibrtqlktbrhwemnbi:Laroca6729@aws-0-sa-east-1.pooler.supabase.com:6543/postgres")



