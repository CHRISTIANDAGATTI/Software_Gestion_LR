import os

# URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:admin@localhost/software_gestion_db")