from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from flask import render_template
from flask import redirect, url_for, session
import requests

app = Flask(__name__)

app.secret_key = 'c7d6bcb92963629d6ceae5c6514492bbc3ba13e29f26a0f6ura'

# Seguridad OWASP: Cabeceras seguras
Talisman(app, content_security_policy=None)

# 1. Configuración de Base de Datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# 2. Modelo de Usuario (Tabla en la DB)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# 3. Crea las tablas automáticamente
with app.app_context():
    db.create_all()

# 4. RUTA DE REGISTRO
@app.route('/registrar', methods=['POST'])
def registrar():
    # Esta línea permite obtener datos tanto de JSON (Postman) como de Formulario (Web)
    if request.is_json:
        datos = request.get_json()
    else:
        datos = request.form

    try:
        hash_password = bcrypt.generate_password_hash(datos['password']).decode('utf-8')
        nuevo_usuario = Usuario(
            username=datos['username'],
            password=hash_password
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        # En lugar de enviar un JSON, lo mandamos al Login
        return redirect(url_for('login')) 
    except Exception as e:
        return "Error: El usuario ya existe", 400
    
# 5. RUTA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            datos = request.get_json()
        else:
            datos = request.form
        
        usuario = Usuario.query.filter_by(username=datos['username']).first()
        
        if usuario and bcrypt.check_password_hash(usuario.password, datos['password']):
            # Guardamos el usuario en la "sesión" para que el servidor lo recuerde
            session['usuario'] = usuario.username
            return redirect(url_for('bienvenida')) # Lo mandamos a la nueva página
        else:
            return "Error: Usuario o contraseña incorrectos", 401
    
    return render_template('login.html')

# 6. RUTA DE BIENVENIDA
@app.route('/bienvenida')
def bienvenida():
    if 'usuario' in session:
        #API KEY de TMDB
        api_key = "fef9f1ee5ad82375662144bc489ca64b" 
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=es-ES&page=1"
        
        try:
            respuesta = requests.get(url)
            datos = respuesta.json()
            peliculas = datos.get('results', [])
        except:
            peliculas = [] # Si la API falla, enviamos una lista vacía para que no explote
            
        return render_template('bienvenida.html', nombre=session['usuario'], peliculas=peliculas)
    
    return redirect(url_for('login'))

# 6. RUTA DE DETALLE
@app.route('/pelicula/<int:id>')
def detalle_pelicula(id):
    if 'usuario' in session:
        api_key = "fef9f1ee5ad82375662144bc489ca64b"
        # Llamamos al endpoint de detalles de la película
        # append_to_response=credits nos permite traer también a los actores
        url = f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=es-ES&append_to_response=credits"
        
        try:
            respuesta = requests.get(url)
            peli = respuesta.json()
            return render_template('detalle.html', peli=peli)
        except:
            return "Error al obtener los detalles de la película", 500
            
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/registrar_page')
def registrar_page():
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)