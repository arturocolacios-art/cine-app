from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user # <-- Asegúrate de añadir UserMixin aquí
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from flask import render_template
from flask import redirect, url_for, session
import requests

app = Flask(__name__)

app.secret_key = 'c7d6bcb92963629d6ceae5c6514492bbc3ba13e29f26a0f6ura'

#Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# OWASP: Cabeceras seguras
Talisman(app, content_security_policy=None)

# 1. Configuración de Base de Datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# OWASP: Seguridad ante inyecciones y contraseñas cifradas
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# 2. Modelo de Usuario (Tabla en la DB)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), default='user') # Puede ser 'user' o 'admin'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 3. Crea las tablas automáticamente
with app.app_context():
    db.create_all()

# 4. RUTA DE REGISTRO
@app.route('/registrar', methods=['POST'])
def registrar():
    if request.is_json:
        datos = request.get_json()
    else:
        datos = request.form

    try:
        # 1. Extraemos los datos correctamente
        username = datos.get('username')
        password = datos.get('password')

        # 2. Creamos el hash con la variable correcta
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # 3. Creamos el usuario usando las variables que acabamos de definir
        #nuevo_usuario = User(username=username, password=hash_password, role='admin')
        nuevo_usuario = User(username=username, password=hash_password, role='user')

        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return redirect(url_for('login')) 

    except Exception as e:
        # Esto te ayudará a ver en la terminal qué error real está pasando
        print(f"Error real: {e}") 
        return f"Error al registrar: {str(e)}", 400
    
# 5. RUTA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            datos = request.get_json()
        else:
            datos = request.form
        
        usuario = User.query.filter_by(username=datos['username']).first()
        
        if usuario and bcrypt.check_password_hash(usuario.password, datos['password']):
            # Guardamos el usuario en la "sesión" para que el servidor lo recuerde
            login_user(usuario)
            session['usuario'] = usuario.username
            return redirect(url_for('bienvenida')) # Lo mandamos a la nueva página
        else:
            return "Error: Usuario o contraseña incorrectos", 401
    
    return render_template('login.html')

# 6. RUTA DE BIENVENIDA
@app.route('/bienvenida')
@login_required # Esto reemplaza el "if 'usuario' in session" por una protección de nivel profesional
def bienvenida():
    # API KEY de TMDB
    api_key = "fef9f1ee5ad82375662144bc489ca64b" 
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=es-ES&page=1"
    
    try:
        respuesta = requests.get(url, timeout=5) # Añadimos timeout por seguridad
        respuesta.raise_for_status() # Verifica si hubo error en la petición
        datos = respuesta.json()
        peliculas = datos.get('results', [])
    except Exception as e:
        print(f"Error en API TMDB: {e}")
        peliculas = [] 
        
    # Pasamos 'current_user' para que el HTML pueda leer el .role que creamos
    return render_template('bienvenida.html', 
                           nombre=current_user.username, 
                           peliculas=peliculas, 
                           user=current_user)

# 7. RUTA DE DETALLE
@app.route('/pelicula/<int:id>')
def detalle_pelicula(id):
    if 'usuario' in session:
        api_key = "fef9f1ee5ad82375662144bc489ca64b"
        # Llamamos al endpoint de detalles de la película
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