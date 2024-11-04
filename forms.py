"""
    Archivo donde se definen los formularios del sistema
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class FormularioRegistro(FlaskForm):    
    nombre          = StringField('Nombre', validators=[DataRequired(), Length(min=3)])
    correo          = EmailField('Correo', validators=[DataRequired(), Email()])
    clave           = PasswordField('Clave', validators=[DataRequired(), EqualTo('confirmar_clave', message="Las claves deben ser iguales.")])
    confirmar_clave = PasswordField('Confirmar clave', validators=[DataRequired()])
    submit          = SubmitField('Registrarme')

class FormularioAcceso(FlaskForm):    
    correo = EmailField('Correo', validators=[DataRequired(), Email()])
    clave  = PasswordField('Clave', validators=[DataRequired()])    
    submit = SubmitField('Acceder')

class FormularioAgregarCita(FlaskForm):
    desc   = StringField('Descripción', validators=[DataRequired(), Length(min=1,max=30)])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Estatus', choices=[
        ('Pendiente', "Pendiente"),
        ('Hecha', 'Hecha'),
        ('Perdida', 'Perdida')
    ])
    submit = SubmitField('Agregar Cita')
