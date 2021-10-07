from flask import render_template, request, flash, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from app import create_app

from app.models import Usuario, Rol, Usuario_Rol, db

app = create_app()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Tienes que iniciar primero sesion"
login_manager.login_message_category = "error"

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return Usuario.query.get(user_id)
    except:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['txtUsuario']
        clave = request.form['txtClave']

        usuarioData = Usuario.query.filter(Usuario.usuLogin == usuario and Usuario.usuPassword == clave).first()

        if (usuarioData):
            login_user(usuarioData)
            flash('Te has logueado correctamente', 'success')
            return redirect(url_for('paginaCliente'))
        else:    
            flash('Datos erroneos', 'error')

    if current_user.is_authenticated:
        flash('Ya te encuentras logeado, si deseas utilizar otra cuenta cierra sesion primero', 'info')
        return redirect(url_for('paginaCliente'))
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['txtUsuario']
        clave = request.form['txtClave']

        usuarioData = Usuario.query.filter(Usuario.usuLogin == usuario).first()

        if (usuarioData):
            flash('ese usuario ya existe', 'error')
        else:
            newUsuario = Usuario(usuario, clave)
            db.session.add(newUsuario)
            db.session.commit()

            flash('Te has registrado correctamente', 'success')
            return redirect(url_for('index'))

    if current_user.is_authenticated:
        flash('Ya te encuentras logeado, si deseas utilizar otra cuenta cierra sesion primero', 'info')
        return redirect(url_for('paginaCliente'))
    else:
        return render_template('register.html')

@app.route('/cliente')
@login_required
def paginaCliente():

    usuarioRol = Usuario_Rol.query.filter(Usuario_Rol.usuId == current_user.usuId).all()
    rolesUsuarioList =  []
    for x in usuarioRol:
        rolesUsuario = Rol.query.filter(Rol.rolId == x.rolId).first()
        if rolesUsuario.rolTipo == "Administrador":
            return redirect('/cliente/Administrador')
        elif rolesUsuario.rolTipo == "Vendedor":
            return redirect('/cliente/Vendedor')
        else:
            return redirect('/cliente/Cliente')

@app.route('/cliente/<tipo>')
def paginaClienteRol(tipo):

    usuarioRol = Usuario_Rol.query.filter(Usuario_Rol.usuId == current_user.usuId).all()
    rolesUsuarioList =  []
    for x in usuarioRol:
        rolesUsuario = Rol.query.filter(Rol.rolId == x.rolId).first()
        rolesUsuarioList.append(rolesUsuario.rolTipo)
    
    if tipo in rolesUsuarioList:

        context = {
            'rolesUsuario'  : rolesUsuarioList,
            'usuarioActual' : current_user,
            'activeRol' : tipo
        }

        return render_template('paginaCliente.html', **context)
    else:
        flash('No tienes este rol', 'error')
        return redirect(url_for('paginaCliente'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))