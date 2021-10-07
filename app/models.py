from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'Categoria'
    catId = db.Column(db.Integer, primary_key=True)
    catTipo = db.Column(db.String(50))
    # Relaciones
    vehiculo = db.relationship('Vehiculo')


    def __init__(self, catTipo):
        self.catTipo = catTipo
    
class DatosPersonales(db.Model):
    __tablename__ = 'DatosPersonales'
    datId = db.Column(db.Integer, primary_key=True)
    datNombre = db.Column(db.String(50))
    datApellido = db.Column(db.String(50))
    datTipoId = db.Column(db.String(20))
    datNumeroId = db.Column(db.String(20))
    datTelefono = db.Column(db.String(20))
    datCorreo = db.Column(db.String(50))
    usuId = db.Column(db.Integer, db.ForeignKey('Usuario.usuId'))
    
    def __init__(self, usuId, datNombre, datApellido, datTipoId, datNumeroId, datTelefono, datCorreo):
        self.usuId = usuId
        self.datNombre = datNombre
        self.datApellido = datApellido
        self.datTipoId = datTipoId
        self.datNumeroId = datNumeroId
        self.datTelefono = datTelefono
        self.datCorreo = datCorreo

class Rol(db.Model):
    __tablename__ = 'Rol'
    rolId = db.Column(db.Integer, primary_key=True)
    rolTipo = db.Column(db.String(50))
    # Relaciones
    usuario_rol = db.relationship('Usuario_Rol', back_populates="rol")

    def __init__(self, rolTipo):
        self.rolTipo = rolTipo
    
class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuario'
    usuId = db.Column(db.Integer, primary_key=True)
    usuLogin = db.Column(db.String(45), nullable=False)
    usuPassword = db.Column(db.String(45), nullable=False)
    # Relaciones
    usuario_rol = db.relationship('Usuario_Rol', back_populates="usuario")
    datosPersonales = db.relationship('DatosPersonales')

    def get_id(self):
        return (self.usuId)
    
    def __init__(self, usuLogin, usuPassword):
        self.usuLogin = usuLogin
        self.usuPassword = usuPassword
        
class Usuario_Rol(db.Model):
    __tablename__ = 'Usuario_Rol'
        
    usuId = db.Column(db.Integer, db.ForeignKey('Usuario.usuId'), primary_key=True)
    rolId = db.Column(db.Integer, db.ForeignKey('Rol.rolId'), primary_key=True)
    # Relaciones
    usuario = db.relationship('Usuario', back_populates="usuario_rol")
    rol = db.relationship('Rol', back_populates = "usuario_rol")
    # SELECT usuario.USUID,usuario.usuLogin,usuario.usuPassword,rol.ROLTIPO FROM usuario 
    # INNER JOIN usuario_rol on usuario.USUID = usuario_rol.USUID 
    # INNER JOIN rol on usuario_rol.ROLID= rol.ROLID 
    # WHERE usulogin = '" + usuario + "'
    def __init__(self,rolId, usuId):
        self.rolId = rolId
        self.usuId = usuId 
    
class Vehiculo(db.Model):
    __tablename__ = 'Vehiculo'
    vehPlaca = db.Column(db.Integer, primary_key=True)
    vehModelo = db.Column(db.Integer)
    vehMarca = db.Column(db.String(50))
    vehEstado = db.Column(db.String(30))
    vehPrecio = db.Column(db.Integer)
    datId = db.Column(db.Integer, db.ForeignKey('DatosPersonales.datId'))
    catId = db.Column(db.Integer, db.ForeignKey('Categoria.catId'))
 
    def __init__(self, datId, catId, vehModelo, vehMarca, vehEstado, vehPrecio):
        self.datId = datId
        self.catId = catId
        self.vehModelo = vehModelo
        self.vehMarca = vehMarca
        self.vehEstado = vehEstado
        self.vehPrecio = vehPrecio