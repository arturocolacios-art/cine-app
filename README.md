🎬 CineApp: Gestión Segura de Cartelera y Roles (SecDevOps)

CineApp es una plataforma web desarrollada con Python (Flask) bajo principios de seguridad SecDevOps. El sistema permite la gestión de usuarios, visualización de películas en tiempo real y un panel de administración protegido mediante roles dinámicos.

🛡️ Arquitectura de Seguridad (OWASP Top 10 Compliance)

Este proyecto ha sido auditado y diseñado para mitigar las vulnerabilidades más críticas según el estándar internacional OWASP:

A01:2021 – Control de Acceso Quebrado: Implementación de RBAC (Role-Based Access Control) con Flask-Login. Solo los usuarios con el rol admin visualizan componentes críticos.

A02:2021 – Fallos Criptográficos: Uso de Flask-Bcrypt para el hashing de contraseñas. Nunca se almacena información sensible en texto plano.

A03:2021 – Inyección: Uso de SQLAlchemy ORM para realizar consultas parametrizadas automáticas, eliminando riesgos de Inyección SQL.

A05:2021 – Configuración de Seguridad Incorrecta: Integración de Flask-Talisman para el hardening de cabeceras HTTP (CSP, XSS Protection, Clickjacking).

🔌 Integración de Servicios Externos (API TMDB)

La aplicación consume datos en tiempo real de The Movie Database (TMDB).

Backend-to-API: Las peticiones se gestionan desde el servidor para proteger la API_KEY.

Resiliencia: Manejo de errores mediante bloques try-except y timeouts para asegurar la disponibilidad si el servicio externo falla.

Privacidad: Se aplica el principio de mínimo privilegio, extrayendo únicamente los campos necesarios del JSON de respuesta (title, poster_path, overview).

🧪 Suite de Pruebas y Validación de Seguridad (Postman)

Se ha implementado una batería de pruebas automatizadas que validan la seguridad en tres niveles críticos:

1. Validación de Acceso y Hardening (POST /login)

Confirma que el sistema procesa credenciales correctamente y que el servidor no revela información técnica sensible (fingerprinting).

pm.test("Estado final exitoso (200 OK)", function () {
    pm.response.to.have.status(200);
});

pm.test("Seguridad: No se revela la versión del servidor", function () {
    // Evita que atacantes conozcan la tecnología exacta (ej. Werkzeug)
    pm.expect(pm.response.headers.get("Server")).to.not.include("Werkzeug");
});


2. Control de Acceso Basado en Roles - RBAC (GET /bienvenida)

Valida que el servidor aplica la lógica de autorización entregando contenido exclusivo al rol Administrador.

pm.test("Verificación de Rol: Interfaz de ADMIN detectada", function () {
    var responseText = pm.response.text();
    pm.expect(responseText).to.include("🛡️ Panel de Control: Administrador");
});


3. Auditoría de Protección de Navegador (Middleware Talisman)

Validamos la presencia de cabeceras críticas inyectadas por el firewall de aplicación.

pm.test("Seguridad: Cabecera X-Frame-Options presente", function () {
    // Mitigación efectiva contra ataques de Clickjacking
    pm.expect(pm.response.headers.has("X-Frame-Options")).to.be.true;
});


📊 Resumen de Resultados de la Auditoría

Categoría

Prueba

Resultado

Riesgo Mitigado

Identidad

Autenticación Segura

PASSED ✅

A07:2021 – Fallos de Identificación

Autorización

Detección de Rol Admin

PASSED ✅

A01:2021 – Acceso Quebrado

Infraestructura

Hardening (Server Header)

PASSED ✅

A05:2021 – Configuración Insegura

Integridad

Protección Clickjacking

PASSED ✅

A04:2021 – Diseño Inseguro

🛠️ Tecnologías y Dependencias

Lenguaje: Python 3.x

Framework: Flask

Base de Datos: SQLite con SQLAlchemy (ORM)

Seguridad: Flask-Bcrypt, Flask-Talisman, Flask-Login

Consumo API: Requests library

Pruebas: Postman API Client

🚀 Instalación y Despliegue Local

Clonar el repositorio.

Crear entorno virtual: python -m venv venv.

Instalar dependencias: pip install -r requirements.txt.

Configurar API Key de TMDB en app.py.

Ejecutar la aplicación: python app.py.

Nota Final: Este proyecto ha sido desarrollado como parte de una formación en SecDevOps, priorizando la seguridad en el ciclo de vida del desarrollo de software (SDLC).
