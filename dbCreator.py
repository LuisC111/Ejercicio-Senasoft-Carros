from app import create_app
from app.models import db, Categoria, DatosPersonales, Rol, Usuario, Usuario_Rol, Vehiculo

app =  create_app()

app.app_context().push()

db.create_all()

categoria1 = Categoria('camperos')
categoria2 = Categoria('automóviles')
categoria3 = Categoria('camionetas')

rol1 = Rol('Administrador')
rol2 = Rol('Vendedor')
rol3 = Rol('Cliente')

usuario1 = Usuario('HectorF25','12345678')
usuario2 = Usuario('DavidsDvm','12345678')
usuario3 = Usuario('Fallen','12345678')

usuarioRol1 = Usuario_Rol(1,1)
usuarioRol2 = Usuario_Rol(2,1)
usuarioRol3 = Usuario_Rol(2,2)
usuarioRol4 = Usuario_Rol(3,2)
usuarioRol5 = Usuario_Rol(3,3)

vehiculo1 = Vehiculo(1235,1,2,'2015','Mazda','Usado',15000)
vehiculo2 = Vehiculo(1123,3,3,'2019','Mazda','Nuevo',25000)

datospersonales1 = DatosPersonales(1, 'Carmila', 'nieto', 'cc', '230123', '1231231', 'camilitarpt@solomillos.com')
datospersonales2 = DatosPersonales(2, 'karmelo', 'vergara', 'cc', '23213', '123213123', 'karamelo@solorojos.com')
datospersonales3 = DatosPersonales(3, 'sileta', 'perulo', 'cc', '213123', '213213213', 'parulosirulo@solomillos.com')

db.session.add(categoria1)
db.session.add(categoria2)
db.session.add(categoria3)
db.session.add(rol1)
db.session.add(rol2)
db.session.add(rol3)
db.session.add(usuario1)
db.session.add(usuario2)
db.session.add(usuario3)
db.session.add(usuarioRol1)
db.session.add(usuarioRol2)
db.session.add(usuarioRol3)
db.session.add(usuarioRol4)
db.session.add(usuarioRol5)
db.session.add(vehiculo1)
db.session.add(vehiculo2)
db.session.add(datospersonales1)
db.session.add(datospersonales2)
db.session.add(datospersonales3)
db.session.commit()