# CineApp: Gestión Segura de Cartelera y Roles (SecDevOps)

**CineApp** es una plataforma web desarrollada con **Python (Flask)** bajo principios de seguridad **SecDevOps**. El sistema permite la gestión de usuarios, visualización de películas en tiempo real y un panel de administración protegido mediante roles dinámicos.

---

## Stack Tecnológico y Herramientas

Para cumplir con los objetivos de **SecDevOps**, se ha integrado un ecosistema de herramientas enfocadas en la robustez, la escalabilidad y, sobre todo, la seguridad proactiva.

---

### Desarrollo (Backend & Frontend)
El núcleo de la aplicación se basa en tecnologías ágiles que permiten una integración fluida de medidas de seguridad.

| Tecnología | Propósito |
| :--- | :--- |
| **Python 3.11** | Lenguaje principal del proyecto. |
| **Flask** | Framework web para el Front-end y la lógica de la API. |
| **Jinja2** | Motor de plantillas para renderizar la interfaz dinámica de forma segura. |
| **SQLite + SQLAlchemy** | Base de datos ligera con ORM para prevenir ataques de **Inyección SQL**. |
| **TMDB API** | Fuente externa para el suministro de datos cinematográficos. |

---

### Seguridad (SecDevOps)
Siguiendo las mejores prácticas de **OWASP**, se han implementado las siguientes capas de protección:

* **Flask-Talisman:** Configuración de cabeceras de seguridad críticas como `CSP`, `HSTS` y `X-Frame-Options`.
  * [Ver implementación en `app/app.py` (Línea 20)](https://github.com/arturocolacios-art/cine-app/blob/main/app/app.py#L20)
* **Flask-Bcrypt:** Hashing avanzado de contraseñas con *salting* para mitigar riesgos de seguridad en credenciales (**OWASP A02**).
* **Flask-Login:** Gestión segura de sesiones de usuario y control de acceso basado en roles (**RBAC**).
* **Python-dotenv:** Desacoplamiento de secretos y credenciales del código fuente mediante variables de entorno.

---

### Virtualización y Despliegue
Garantizamos que el entorno de ejecución sea reproducible y esté aislado.

* **Docker:** Contenerización de la aplicación para asegurar portabilidad y aislamiento de procesos.
* **Python venv:** Entornos virtuales para la gestión estricta de dependencias en desarrollo local.

---

### Pruebas y Auditoría
Validación continua de la integridad del código y la seguridad de los endpoints.

* **Postman:** Suite para pruebas de integración y auditoría técnica de cabeceras de seguridad.
* **Unittest:** Framework nativo para la ejecución de pruebas unitarias sobre la lógica de negocio.

---

### Automatización y Control
* **GitHub Actions:** Pipeline de **CI/CD** para la construcción automática de imágenes y validación de Dockerfiles.
* **Git / GitHub:** Control de versiones y flujo de trabajo basado en ramas para asegurar la trazabilidad del código.

## Arquitectura de Seguridad (OWASP Top 10 Compliance)

Este proyecto ha sido auditado y diseñado para mitigar las vulnerabilidades más críticas según el estándar internacional **OWASP**:

* **[A01:2025 – Control de Acceso Quebrado](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/)**
Implementación de **RBAC** (*Role-Based Access Control*) mediante `Flask-Login`. Se garantiza que únicamente los usuarios con el rol `admin` tengan acceso a componentes críticos del sistema.
* **[A02:2025 – Configuración de Seguridad Incorrecta](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/)**
  Integración de `Flask-Talisman` para el *hardening* de cabeceras HTTP. Esta capa de seguridad implementa políticas de CSP (Content Security Policy), protección contra XSS y prevención de ataques de Clickjacking.
* **[A04:2025 – Fallos Criptográficos](https://owasp.org/Top10/2025/A03_2025-Cryptographic_Failures/)**
  Implementación de `Flask-Bcrypt` para el hashing robusto de contraseñas. Se garantiza que la información sensible jamás se almacene en texto plano, utilizando algoritmos de derivación de claves seguros.
* **[A05:2025 – Inyección](https://owasp.org/Top10/2025/A04_2025-Injection/)**
  Uso de **SQLAlchemy ORM** para la abstracción de base de datos. Esto permite realizar consultas parametrizadas automáticas por defecto, eliminando de raíz el riesgo de ataques de Inyección SQL.


---

## Cumplimiento de Seguridad (OWASP API Top 10)

Este proyecto ha sido diseñado siguiendo los estándares de **OWASP API Security 2023** para mitigar los riesgos más críticos en servicios web:

* **[API1:2023 – Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)** Control de acceso basado en roles (RBAC) con Flask-Login para asegurar que un usuario solo acceda a sus propios datos.
* **[API2:2023 – Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)** Protección contra fuerza bruta y robo de credenciales mediante el hashing robusto de **Bcrypt**.
* **[API8:2023 – Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)** Eliminación de información sensible en errores de producción y uso de cabeceras `CSP`, `HSTS` y `X-Frame-Options` vía **Flask-Talisman**.
* **[API10:2023 – Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)** Validación estricta de los datos recibidos de la API externa (TMDB) antes de ser procesados por el motor de plantillas **Jinja2**.

---

# Integración de Servicios Externos (API TMDB)

La aplicación consume datos en tiempo real de **The Movie Database (TMDB)** siguiendo buenas prácticas de seguridad:

1.  **Backend-to-API:** Las peticiones se gestionan desde el servidor para proteger la `API_KEY`.
2.  **Resiliencia:** Manejo de errores mediante bloques `try-except` y *timeouts* para asegurar la disponibilidad si el servicio externo falla.
3.  **Privacidad:** Se aplica el principio de **mínimo privilegio**, extrayendo únicamente los campos necesarios del JSON de respuesta (`title`, `poster_path`, `overview`).

---

## Suite de Pruebas y Validación de Seguridad (Postman)

Se ha implementado una batería de pruebas automatizadas que validan la seguridad en tres niveles críticos:

### 1. Validación de Acceso y Hardening (`POST /login`)
Confirma que el sistema procesa credenciales correctamente y que el servidor no revela información técnica sensible (*fingerprinting*).

```javascript
pm.test("Estado final exitoso (200 OK)", function () {
    pm.response.to.have.status(200);
});

pm.test("Seguridad: No se revela la versión del servidor", function () {
    // Evita que atacantes conozcan la tecnología exacta (ej. Werkzeug)
    pm.expect(pm.response.headers.get("Server")).to.not.include("Werkzeug");
});
```

### 2. Control de Acceso Basado en Roles - RBAC (GET /bienvenida)

Valida que el servidor aplica la lógica de autorización entregando contenido exclusivo al rol Administrador.

```javascript
pm.test("Verificación de Rol: Interfaz de ADMIN detectada", function () {
    var responseText = pm.response.text();
    pm.expect(responseText).to.include("Panel de Control: Administrador");
});
```

### 3. Auditoría de Protección de Navegador (Middleware Talisman)

Validamos la presencia de cabeceras críticas inyectadas por el firewall de aplicación.

```javascript
pm.test("Seguridad: Cabecera X-Frame-Options presente", function () {
    // Mitigación efectiva contra ataques de Clickjacking
    pm.expect(pm.response.headers.has("X-Frame-Options")).to.be.true;
});
```

## Entorno de Desarrollo y Aislamiento

Siguiendo las buenas prácticas de desarrollo y los requisitos de la asignatura, se ha utilizado un **entorno virtual (`venv`)** para aislar las dependencias del proyecto. Esto garantiza que las librerías de `CineApp` no entren en conflicto con otros proyectos y permite una gestión limpia de los requisitos.

### Configuración del entorno:
1. **Creación**: `python -m venv venv`
2. **Activación**:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. **Instalación de dependencias**: `pip install -r requirements.txt`

## Instalación y Despliegue Local

**1. Clonar el repositorio:**

```bash
git clone <repo_url>
cd cineapp
```

**2. Crear entorno virtual:**

```bash
Crear entorno virtual: python -m venv venv.
```

**3. Instalar dependencias:**

```bash
pip install -r requirements.txt
```

**4. Ejecutar la aplicación:**

```bash
Ejecutar la aplicación: python app.py.
```
