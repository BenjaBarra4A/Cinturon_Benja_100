"""
    Archivo de modelos de bases de datos
"""
from app import db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash #seguridad
from datetime import date



#Modelos de bases de datos
class Usuario(db.Model, UserMixin):
    __tablename__  = "usuarios"
    id             = db.Column(db.Integer, primary_key=True)
    nombre         = db.Column(db.String(255), nullable=True)
    correo         = db.Column(db.String(255),nullable=True,unique=True)
    clave          = db.Column(db.String(255),nullable=True)

    cita           = db.relationship('Cita', back_populates='usuario')
    
    def establecer_clave(self, clave):
        self.clave = generate_password_hash(clave)
    def chequeo_clave(self, clave):
        return check_password_hash(self.clave, clave)
    #función para obetener todos los registros de la db
    @staticmethod
    def obtener_todos():
        all_items = db.session.execute(db.select(Usuario)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)   
        print("Items de consulta:",all_items_list)
        return all_items_list     
    @staticmethod 
    def obtener_por_correo(correo):
        usuario = Usuario.query.filter_by(correo=correo).first()
        print(f"Consultando por el usuario {usuario} en db")
        return usuario
    @staticmethod
    def obtener_por_id(id):
        print(f"Consultando por el usuario con id{id} en db")
        return Usuario.query.get(id)

class Cita(db.Model):
    __tablename__ = "cita"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    fecha = db.Column(db.DATE, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='cita')

    @staticmethod
    def obtener_todos():
        all_items = db.session.execute(db.select(Cita)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)   
        print("Items de consulta:",all_items_list)
        return(all_items_list) 

    @staticmethod
    def obtener_como_opciones():
        all_items = db.session.execute(db.select(Cita)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append((item.id,item.nombre))   
        print("Items de consulta:",all_items_list)
        return(all_items_list)
    
    @staticmethod
    def obtener_citas_pasadas(usuario_id):
        fecha_actual = date.today()
        return Cita.query.filter(
            Cita.usuario_id == usuario_id, Cita.fecha < fecha_actual).all()