""" 
Maneja el control sobre la información de la vista
y los modelos de bases de datos
"""
from models import db, Usuario, Cita

class ControladorUsuarios:
    @staticmethod
    def crear_usuario(nombre,correo,clave):
        usuario = Usuario()
        usuario.nombre = nombre 
        usuario.correo = correo 
        usuario.establecer_clave(clave)
            
        #Agregamos a la base datos
        db.session.add(usuario)
        db.session.commit()
        return usuario
    #def editar_usuario()
    #def obtener_usuarios()
    #def borrar_usuario()

class ControladorCitas:
    @staticmethod
    def crear_cita(nombre, fecha, status, usuario_id):
        nueva_cita = Cita(nombre=nombre, fecha=fecha, status=status, usuario_id=usuario_id)
        db.session.add(nueva_cita)
        db.session.commit()

    @staticmethod
    def obtener_todos():
        return Cita.query.all()