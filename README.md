# Password Manager API & Frontend

Este repositorio contiene el código fuente de una aplicación web de gestión de contraseñas. Se ha puesto énfasis en la seguridad, la arquitectura de backend y las buenas prácticas de desarrollo.

La aplicación consta de:
- Un **backend RESTful** construido con **Python (FastAPI)** que gestiona la lógica de negocio, la autenticación y el almacenamiento seguro de datos.
- Un **frontend SPA** construido con **React (Vite)** que consume la API y proporciona una UI para interactuar con la aplicación.
- **Contenerización completa** con **Docker**.

## Características Principales

### Backend (FastAPI)
- **Autenticación:** Sistema de registro y login basado en tokens **JWT**.
- **Gestión de Vault (CRUD):** Funcionalidad completa para crear, leer, actualizar y eliminar credenciales.
- **Seguridad:**
    - Las contraseñas de los usuarios se almacenan **hasheadas** (bcrypt).
    - Las contraseñas del vault se almacenan **cifradas** (Fernet).
- **Recuperación de Contraseña:** Flujo completo para el reseteo de contraseñas mediante token.
- **Búsqueda y Filtrado:** Búsqueda de texto libre y filtrado por URL en el vault del usuario.
- **Testing:** Tests unitarios con `pytest` para asegurar el funcionamiento de los endpoints.

### Frontend (React)
- **Interfaz:** Construido con React y Vite.
- **Gestión de Estado de Autenticación:** Rutas protegidas que redirigen a los usuarios no autenticados.
- **Enrutamiento:** Navegación entre páginas de Login, Register, Recuperación de Contraseña y el vault principal.
- **Interfaz para CRUD:** Modal interactivo para añadir, ver, editar y eliminar credenciales.

## Tecnologías Utilizadas

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Pydantic, Passlib, python-jose, Cryptography.
- **Frontend:** React 18, Vite, React Router, Axios, CSS.
- **Base de Datos:** SQLite.
- **Testing:** Pytest, HTTPX.
- **Contenerización:** Docker.

## Instalación y ejecución

Para ejecutar la aplicación recomiendo **Docker**, ya que gestiona tanto el backend como sus dependencias en un entorno aislado.

### Prerrequisitos
- [Docker](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.
- [Node.js](https://nodejs.org/) (v18 o superior) y `npm` para ejecutar el frontend localmente.
- Git.

### 1. Clonar el Repositorio
```bash
git clone https://github.com/julialeu/password-manager.git
cd password-manager
```

### 2. Configuración de env
El backend requiere dos secret keys para funcionar.
1.  Crea un archivo llamado `.env` en la raíz del proyecto.
2.  Copia el contenido del archivo `.env.example` y pégalo en  `.env`.
3.  **Genera las propias secret keys:**
    - Para `SECRET_KEY` (usada para JWT), puedes usar un generador online
      ```
    - Para `ENCRYPTION_KEY` (usada para cifrar datos), ejecuta este comando de Python:
      ```bash
      python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
      ```
4.  Reemplaza los valores del `.env` con las keys que has generado.

### 3. Ejecutar el Backend con Docker
Asegúrate de que la BD se inicialice correctamente la primera vez.
```bash
# Paso 1: Inicializar la BD (solo la primera vez o si cambias los modelos)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.db.init_db

# Paso 2: Construir la imagen de Docker
docker build -t password-manager-api .

# Paso 3: Ejecutar el contenedor
# (Usa $(pwd) en PowerShell/Linux/macOS, o %cd% en CMD de Windows)
docker run -d -p 8000:8000 --env-file .env --name password-manager-container -v "$(pwd)/password_manager.db:/app/password_manager.db" password-manager-api
```
MIRAR `http://localhost:8000`!

### 4. Ejecutar el Frontend
Abre una **nueva terminal** en la raíz del proyecto.
```bash
# Navega a la carpeta del frontend
cd frontend

# Instala las dependencias
npm install

# Inicia el servidor de desarrollo
npm run dev
```
El frontend está disponible en `http://localhost:5173`.

### 5. Comandos Útiles de Docker
- **Ver contenedores en ejecución:** `docker ps`
- **Ver todos los contenedores (incluidos los detenidos):** `docker ps -a`
- **Ver los logs del backend:** `docker logs -f password-manager-container`
- **Detener el contenedor:** `docker stop password-manager-container`
- **Iniciar un contenedor detenido:** `docker start password-manager-container`

---

## Guía de Pruebas

### Pruebas del Backend con Swagger

Una vez que el backend esté corriendo en Docker, puedes probar los endpoints.
1.  Abre el navegador y ve a **(http://localhost:8000/docs)**.
2.  **Registro:**
    - En `Users > POST /users/`, crea un nuevo usuario (ej: `test@test.com`, `password123`).
3.  **Login:**
    - En `Login > POST /login/token`, inicia sesión con las credenciales del nuevo usuario.
    - Copia el `access_token` que recibes en la respuesta.
4.  **Autorización:**
    - Haz clic en el botón verde **"Authorize"** en la parte superior derecha.
    - Pega el `access_token` en el campo `value` y autoriza. El candado se cerrará.
5.  **CRUD del Vault:**
    - Ahora puedes usar todos los endpoints de `Vault` (`POST`, `GET`, `PUT`, `DELETE`) para gestionar las credenciales.
6.  **Recuperación de Contraseña:**
    - En `Login > POST /login/password-recovery/{email}`, introduce el email de tu usuario.
    - Revisa los logs de Docker (`docker logs password-manager-container`) para encontrar el token de reseteo simulado.
    - En `Login > POST /login/reset-password/`, usa ese token para establecer una nueva contraseña.

### Pruebas del Frontend

Con el backend corriendo en Docker y el frontend en `npm run dev`, puedes probar el flujo completo como un usuario final.
1.  Abre **(http://localhost:5173/)**.
2.  Serás redirigido a la página de **Login**.
3.  **Registro:**
    - Haz clic en el enlace "Create Account".
    - Podrás hacer login con el usuario creado. Se redirecciona al vault.
4.  **Gestión en la Bóveda:**
    - Usa el botón "Add Password" para abrir el modal y crear un nuevo item.
    - Utiliza el campo de búsqueda para filtrar tus items.
    - Haz clic en "Edit" en un item para abrir el modal y modificar sus datos.
    - Dentro del modal de edición, haz clic en "View" para cargar y mostrar la contraseña descifrada.
    - Usa el botón "Delete" para borrar un item.
5.  **Cerrar Sesión:**
    - El botón "Logout" debería borrar tu token y redirigirte a la página de login.
6.  **Recuperación de Contraseña:**
    - En la página de login, haz clic en "Forgot Password?".
    - Sigue el flujo introduciendo tu email.
    - Copia el token de los logs de Docker y construye la URL manualmente en tu navegador: `http://localhost:5173/reset-password?token=TU_TOKEN_AQUI`.
    - Establece la nueva contraseña y verifica que puedes hacer login con ella.


### Enlaces al proyecto

**A) Enlace al front:**
*   `https://password-manager-julia.netlify.app`

**B) Enlace a la documentación de la API (Swagger):**
*   `https://password-manager-api-julia.onrender.com/docs`

**C) Código fuente en Github:**
*   `https://github.com/julialeu/password-manager`

#### **Guía de pruebas para la aplicación desplegada**

**Nota Importante:** El backend está desplegado en el plan gratuito de Render, por lo que la primera petición a la API puede tardar entre 30 y 50 segundos mientras el servicio se "despierta".

**Flujo Principal (Registro y CRUD):**

1.  **Acceder a la aplicación:**
    *   Abre el siguiente enlace en tu navegador:
        **(https://password-manager-julia.netlify.app)**
    *   Serás redirigido/a a la página de Login.

2.  **Crear una nueva cuenta:**
    *   Como la BD es nueva, no hay usuarios. Haz clic en el enlace **"Create Account"**.
    *   Al registrarte, serás automáticamente autenticado/a y redirigido/a a tu vault personal, que estará vacía.

3.  **Gestión del vault:**
    *   **Añadir:** Haz clic en el botón **"Add Password"**. Se abrirá un modal. Rellena los campos obligatorios y guarda. El nuevo item aparecerá en la lista.
    *   **Buscar:** Utiliza el campo de búsqueda para filtrar los items por nombre de usuario, URL o notas.
    *   **Editar y der detalle:** Haz clic en **"Edit"** en cualquier item.
        *   Se abrirá el modal con los datos.
        *   Haz clic en el botón **"View"** junto al campo de la contraseña. Esto realizará una llamada a la API para obtener la contraseña descifrada y mostrarla.
        *   Puedes modificar cualquier campo y guardar los cambios.
    *   **Eliminar:** Haz clic en **"Delete"**. Aparecerá una confirmación. Al aceptar, el item desaparecerá de la lista.

4.  **Cerrar sesión:**
    *   Haz clic en **"Logout"**. Serás redirigido/a a la página de Login y tu sesión se cerrará de forma segura.

**Flujo de Recuperación de Contraseña:**

Este flujo requiere simular la recepción de un email, ya que no se ha configurado un servicio de envío de correos real.

1.  **Solicitar el Reseteo:**
    *   En la página de Login, haz clic en **"¿Forgot Password?"**.
    *   Introduce el email de la cuenta que acabas de crear y haz clic en "Send".

2.  **Obtener el token:**
    *   Esta acción ha generado un token en los logs del servidor del backend.
    *   **Nota importante:** El flujo completo está implementado en el backend y puede ser verificado en el código (`/app/api/endpoints/login.py`) o probado en el entorno local.*

3.  **Establecer la Nueva Contraseña:**
    *   El usuario navegaría a una URL con el token ( `login/reset-password?token=...`).
    *   En la página, introduciría la nueva contraseña y la guardaría.
