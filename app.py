# app.py: módulo principal de la aplicación.

from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

# Iniciación y configuración de la app
app = Flask(__name__) 
app.config["SECRET_KEY"] = "mi clave!"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/cinturon_negro"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth"

# Importación de módulos propios
from forms import FormularioRegistro, FormularioAcceso, FormularioAgregarCita
from models import Usuario, Cita
from controllers import ControladorUsuarios, ControladorCitas

# Inicialización de versiones de la base de datos
Migrate(app, db)

# Inicialización de login_manager y configuración
@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(int(user_id))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Rutas
@app.route("/")
def auth(form_registro=None, form_acceso=None):
    if current_user.is_authenticated:
        return redirect("/home")
    
    if form_registro is None:
        form_registro = FormularioRegistro()
    if form_acceso is None: 
        form_acceso = FormularioAcceso()
    return render_template("auth.html", form_registro=form_registro, form_acceso=form_acceso)

@app.route("/register", methods=["POST"])
def register():
    form = FormularioRegistro()
    error = None 
    if form.validate_on_submit():
        nombre = form.nombre.data
        correo = form.correo.data 
        clave = form.clave.data 
        usuario = Usuario().obtener_por_correo(correo)
        if usuario is not None:
            error = f"El correo {correo} ya se encuentra registrado"
            flash(error)
            return redirect("/")
        else:
            ControladorUsuarios().crear_usuario(nombre, correo, clave)
            return redirect("/home")
    else:
        flash("Form inválido")
        return auth(form_registro=form)

@app.route("/login", methods=["POST"])
def login():
    form_acceso = FormularioAcceso()
    if form_acceso.validate_on_submit():
        usuario = Usuario().obtener_por_correo(form_acceso.correo.data)
        if usuario is not None and usuario.chequeo_clave(form_acceso.clave.data):
            login_user(usuario)
            return redirect("/home")
        else:
            flash("Credenciales inválidas")
            return redirect("/")
    
@app.route("/logout")
def logout():
    logout_user()
    flash("El usuario ha cerrado sesión")
    return redirect("/")

@app.route("/home")
@login_required
def home():
    citas_pasadas = Cita.obtener_citas_pasadas(current_user.id)  
    formulario_cita = FormularioAgregarCita() 
    citas = Cita.query.filter_by(usuario_id=current_user.id).all()
    return render_template("index.html", formulario_cita=formulario_cita, citas=citas, citas_pasadas=citas_pasadas)

@app.route("/agregar_cita", methods=["GET", "POST"])
@login_required
def agregar_cita():
    formulario = FormularioAgregarCita() 
    if formulario.validate_on_submit():
        nombre = formulario.desc.data
        fecha = formulario.fecha.data
        status = formulario.status.data
        usuario_id = current_user.id  

        nueva_cita = Cita(nombre=nombre, fecha=fecha, status=status, usuario_id=usuario_id)
        db.session.add(nueva_cita) 
        db.session.commit() 

        flash("Cita agregada exitosamente", "success")  
        return redirect(url_for('home'))

    return render_template("agregar_cita.html", formulario=formulario)

@app.route("/editar_cita/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cita(id):
    cita = Cita.query.get_or_404(id) 
    formulario = FormularioAgregarCita()

    if formulario.validate_on_submit():
        cita.nombre = formulario.desc.data
        cita.fecha = formulario.fecha.data
        cita.status = formulario.status.data
        
        db.session.commit() 
        flash("Cita actualizada exitosamente", "success")
        return redirect(url_for('home'))

    formulario.desc.data = cita.nombre
    formulario.fecha.data = cita.fecha
    formulario.status.data = cita.status

    return render_template("editar_cita.html", formulario=formulario, cita=cita)
@app.route("/eliminar_cita/<int:id>", methods=["GET"])
@login_required
def eliminar_cita(id):
    cita = Cita.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    flash("Cita eliminada exitosamente", "success")
    return redirect(url_for('home'))