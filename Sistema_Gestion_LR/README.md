# 📦 Software de Gestion LR

Sistema de gestión comercial modular para control de stock, ventas, compras, clientes y proveedores.

- **Backend:** FastAPI + SQLAlchemy + Pydantic + MySQL  
- **Frontend:** Angular puro (sin Angular Material)  
- **Base de Datos:** MySQL  

---


## 🚀 Cómo levantar el proyecto

### 🔥 1. Configurar la base de datos
Crear la base de datos en MySQL:

```sql
CREATE DATABASE commerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Actualizar la cadena de conexión en:

```
backend/app/core/config.py
```

Ejemplo:

```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost/commerce_db"
```

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