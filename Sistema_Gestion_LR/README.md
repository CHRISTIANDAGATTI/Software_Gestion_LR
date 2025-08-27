# 📦 Software de Gestión LR

Sistema de gestión comercial modular multitenant para control de stock, ventas, compras, clientes y proveedores.

- **Backend:** FastAPI + SQLAlchemy + Pydantic + PostgreSQL (Supabase)
- **Frontend:** Angular + Supabase Auth
- **Base de Datos:** PostgreSQL (Supabase)
- **Despliegue:** Render (Backend y Frontend)
- **Autenticación:** Supabase Auth con multitenancy

---

## 🚀 Despliegue en Producción (Render + Supabase)

### 🔥 1. Configurar Supabase

#### 1.1 Crear proyecto en Supabase
1. Ir a [supabase.com](https://supabase.com) y crear una cuenta
2. Crear nuevo proyecto
3. Anotar la URL del proyecto y la clave anónima (anon key)

#### 1.2 Configurar tablas
Ejecutar estos SQL en el editor SQL de Supabase:


### 🌐 2. Desplegar Backend en Render

#### 2.1 Preparar repositorio
1. Subir código a GitHub
2. Asegurar que `requirements.txt` esté actualizado

#### 2.2 Crear Web Service en Render
1. Ir a [render.com](https://render.com) y crear cuenta
2. Conectar repositorio de GitHub
3. Crear nuevo "Web Service"
4. Configurar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** `backend`

#### 2.3 Variables de entorno en Render
```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu_clave_anonima_de_supabase
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/database
```

### 🖥️ 3. Desplegar Frontend en Render

#### 3.1 Configurar environment.prod.ts
```typescript
export const environment = {
  production: true,
  supabaseUrl: 'https://tu-proyecto.supabase.co',
  supabaseAnonKey: 'tu_clave_anonima_de_supabase'
};
```

#### 3.2 Crear Static Site en Render
1. En Render, crear nuevo "Static Site"
2. Conectar mismo repositorio
3. Configurar:
   - **Build Command:** `npm install && ng build --configuration=production`
   - **Publish Directory:** `dist/frontend`
   - **Root Directory:** `frontend`

### 🔧 4. Configuración CORS
En el backend (`app/main.py`), asegurar CORS para el dominio de Render:

```python
origins = [
    "https://tu-frontend.onrender.com",
    "http://localhost:4200",
]
```

---

## 🛠️ Desarrollo Local

### ⚙️ 1. Levantar el Backend (FastAPI)
```bash
cd backend
python -m venv mientorno
mientorno\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 🌐 2. Levantar el Frontend (Angular)
```bash
cd frontend
npm install
ng serve
```

---

## 🛠️ Tecnologías utilizadas

| Componente           | Tecnología                    |
|----------------------|-------------------------------|
| **Backend**          | FastAPI, SQLAlchemy           |
| **Frontend**         | Angular + Supabase JS         |
| **Base de Datos**    | PostgreSQL (Supabase)         |
| **Autenticación**    | Supabase Auth                 |
| **ORM**              | SQLAlchemy                    |
| **Validación**       | Pydantic                      |
| **Despliegue**       | Render                        |
| **Multitenancy**     | Row Level Security (RLS)      |

---

## 📌 Características

- ✅ **Multitenancy:** Cada empresa tiene sus datos separados
- ✅ **Autenticación:** Login/registro con Supabase Auth
- ✅ **Gestión de Stock:** Categorías, productos, inventario
- ✅ **CRM:** Clientes y proveedores
- ✅ **Roles:** Admin y usuarios por empresa
- ✅ **Seguridad:** Row Level Security (RLS) en Supabase
- ✅ **Escalabilidad:** Preparado para módulos de compras/ventas

---

## 🔐 Flujo de Multitenancy

1. **Registro:** Usuario se registra y se asigna al tenant "Demo"
2. **Solicitud:** Usuario puede solicitar acceso a su empresa real
3. **Aprobación:** Admin aprueba y crea/asigna tenant empresarial
4. **Aislamiento:** Todos los datos quedan separados por `tenant_id`
5. **Seguridad:** RLS garantiza que usuarios solo vean datos de su empresa

---

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---