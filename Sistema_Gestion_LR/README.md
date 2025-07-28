# 📦 Software de Gestión LR

Sistema de gestión comercial modular para control de stock, ventas, compras, clientes y proveedores.

- **Backend:** FastAPI + SQLAlchemy + Pydantic + PostgreSQL (Supabase)
- **Frontend:** Angular puro (sin Angular Material)
- **Base de Datos:** PostgreSQL (Supabase)

---

## 🚀 Cómo levantar el proyecto

### 🔥 1. Configurar la base de datos en Supabase
Crea tu proyecto y base de datos en Supabase.

Obtén la cadena de conexión en:

```
backend/app/core/config.py
```

Ejemplo:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BASE"
```

Usa los datos que te da Supabase en Settings > Database.

---

### ⚙️ 2. Levantar el Backend (FastAPI)
Entrar a la carpeta backend:

```bash
cd backend
```

Crear entorno virtual:

```bash
python -m venv mientorno
```

Activar entorno virtual:

```bash
mientorno\Scripts\activate
```

Instalar dependencias:
```bash
pip install -r requirements.txt
```

Instala el driver de PostgreSQL si no lo tienes:
```bash
pip install psycopg2-binary
```

Activar backend:
```bash
uvicorn app.main:app --reload
```

Acceder a la documentación automática de la API:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 🌐 3. Levantar el Frontend (Angular)
Entrar a la carpeta frontend:

```bash
cd frontend
```

Instalar dependencias:

```bash
npm install
```

Levantar servidor Angular:

```bash
ng serve
```

Acceder a la aplicación:  
[http://localhost:4200](http://localhost:4200)

---

## 🛠️ Tecnologías utilizadas

| Componente       | Tecnología          |
|-------------------|---------------------|
| **Backend**       | FastAPI, SQLAlchemy |
| **Frontend**      | Angular             |
| **Base de Datos** | MySQL               |
| **ORM**           | SQLAlchemy          |
| **Validación**    | Pydantic            |

---

## 📌 Notas

- El proyecto está preparado para crecer con módulos: `stock`, `proveedores`, `clientes`, `compras`, `ventas`.
- Todo el código está organizado de forma modular para facilitar el mantenimiento y la escalabilidad.
- El entorno virtual Python se encuentra dentro de la carpeta `backend/venv`.

---