import pytest
from app import app
@pytest.fixture
def client():
    """Fixture que prepara el cliente de pruebas de Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    """Prueba: La página de inicio debe redirigir a HTTPS/Login (302) o dar 200 si seguimos"""
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200

def test_login_page_content(client):
    """Prueba: Verificar que la página de login contiene el texto esperado"""
    response = client.get('/login', follow_redirects=True)
    assert b'Login' in response.data

def test_security_headers(client):
    """Prueba de SecDevOps: Verificar cabeceras de seguridad de Talisman"""
    response = client.get('/', follow_redirects=True)
    # Comprobamos que existan cabeceras de protección clave
    assert 'X-Content-Type-Options' in response.headers
    assert 'X-Frame-Options' in response.headers