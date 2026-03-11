# 🎬 CineApp: Gestión Segura de Cartelera y Roles (SecDevOps)

**CineApp** es una plataforma web desarrollada con **Python (Flask)** bajo principios de seguridad **SecDevOps**. El sistema permite la gestión de usuarios, visualización de películas en tiempo real y un panel de administración protegido mediante roles dinámicos.

---

## 🛡️ Arquitectura de Seguridad (OWASP Top 10 Compliance)

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

## 🔌 Integración de Servicios Externos (API TMDB)

La aplicación consume datos en tiempo real de **The Movie Database (TMDB)** siguiendo buenas prácticas de seguridad:

1.  **Backend-to-API:** Las peticiones se gestionan desde el servidor para proteger la `API_KEY`.
2.  **Resiliencia:** Manejo de errores mediante bloques `try-except` y *timeouts* para asegurar la disponibilidad si el servicio externo falla.
3.  **Privacidad:** Se aplica el principio de **mínimo privilegio**, extrayendo únicamente los campos necesarios del JSON de respuesta (`title`, `poster_path`, `overview`).

---

## 🧪 Suite de Pruebas y Validación de Seguridad (Postman)

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
    pm.expect(responseText).to.include("🛡️ Panel de Control: Administrador");
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

### 📊 Resumen de Resultados de la Auditoría

| Categoría | Prueba | Resultado | Riesgo Mitigado |
| :--- | :--- | :--- | :--- |
| **Identidad** | Autenticación Segura | <code>PASSED ✅</code> | A07:2025 – Fallos de Identificación |
| **Autorización** | Detección de Rol Admin | <code>PASSED ✅</code> | A01:2025 – Acceso Quebrado |
| **Infraestructura** | Hardening (Server Header) | <code>PASSED ✅</code> | A05:2025 – Configuración Insegura |
| **Integridad** | Protección Clickjacking | <code>PASSED ✅</code> | A04:2025 – Diseño Inseguro |

## 🛠️ Resolución de Problemas (Troubleshooting)

Durante el desarrollo y despliegue se detectaron y corrigieron los siguientes incidentes técnicos:

### ❌ `NameError: 'Usuario' is not defined`
* **Causa:** Conflicto de nomenclatura entre la clase del modelo y la referencia en la ruta.
* **Solución:** Reestructuración de las importaciones de los modelos SQLAlchemy y estandarización del nombre de la clase a `User`.

---

### ❌ `AttributeError: 'Flask' object has no attribute 'login_manager'`
* **Causa:** Falta de inicialización del objeto `LoginManager` en el contexto de la app.
* **Solución:** Inicialización correcta de `Flask-Login` mediante `login_manager.init_app(app)` antes del procesamiento de rutas protegidas.

## 🚀 Instalación y Despliegue Local

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
