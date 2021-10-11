from flask import render_template, request, Response, flash, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from fpdf import FPDF
from sqlalchemy.sql.elements import Null

from app import create_app

from app.models import Categoria, DatosPersonales, Usuario, Rol, Usuario_Rol, Vehiculo, db

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

        return render_template('paginaCliente.html', **context, usuarioId = str(current_user.usuId))
    else:
        flash('No tienes este rol', 'error')
        return redirect(url_for('paginaCliente'))

@app.route('/cliente/<tipo>/Vehiculos')
@login_required
def clienteVehiculo(tipo):

    datosUsuario = DatosPersonales.query.filter(DatosPersonales.datId == current_user.usuId).all()
    vehiculoUsuario = db.session.query(Vehiculo,Categoria).join(Categoria,DatosPersonales).filter(DatosPersonales.datId == current_user.usuId).all()

    usuarioRol = Usuario_Rol.query.filter(Usuario_Rol.usuId == current_user.usuId).all()
    rolesUsuarioList =  []
    for x in usuarioRol:
        rolesUsuario = Rol.query.filter(Rol.rolId == x.rolId).first()
        rolesUsuarioList.append(rolesUsuario.rolTipo)

    if tipo in rolesUsuarioList:

        context = {
            'listaVehiculosU' : vehiculoUsuario,
            'rolesUsuario'  : rolesUsuarioList,
            'usuarioActual' : current_user,
            'activeRol' : tipo
        }

        return render_template('paginaCliente.html', **context, usuarioId = str(current_user.usuId))
    else:
        flash('No tienes este rol', 'error')
        return redirect(url_for('paginaCliente'))

@app.route('/cliente/<tipo>/VehiculosReg', methods=['GET', 'POST'])
@app.route('/cliente/<tipo>/VehiculosReg/<vehId>', methods=['GET', 'POST'])
@login_required
def vendedorVehiculo(tipo, vehId = None):

    if request.method == 'POST' and vehId == '0':
        placa = request.form['vehPlaca']
        datoId = request.form['datId']
        cateId = request.form['catId']
        modelo = request.form['vehModelo']
        marca = request.form['vehMarca']
        estado = request.form['vehEstado']
        precio = request.form['vehPrecio']

        print(datoId)


        vehiculoData = Vehiculo.query.filter(Vehiculo.vehPlaca == placa).first()

        if (vehiculoData):
            flash('esa placa ya existe', 'error')
        else:
            if datoId == '':
                datoId = None
                newVehiculo = Vehiculo(placa,datoId,cateId,modelo,marca,estado,precio)
                db.session.add(newVehiculo)
                db.session.commit()
                print(datoId)
            else:
                newVehiculo = Vehiculo(placa,datoId,cateId,modelo,marca,estado,precio)
                db.session.add(newVehiculo)
                db.session.commit()

        flash('Datos almacenados correctamente', 'success')
        return redirect("/cliente/"+tipo+"/VehiculosReg")

    elif request.method == 'POST' and vehId:

        placa = request.form['vehPlaca']
        datoId = request.form['datId']
        cateId = request.form['catId']
        modelo = request.form['vehModelo']
        marca = request.form['vehMarca']
        estado = request.form['vehEstado']
        precio = request.form['vehPrecio']

        updateVehiculo = Vehiculo.query.filter(Vehiculo.vehPlaca == placa).first()

        if(datoId == ''):
            datoId = Null
            updateVehiculo.cateId = cateId
            updateVehiculo.vehModelo = modelo
            updateVehiculo.vehMarca = marca
            updateVehiculo.vehEstado = estado
            updateVehiculo.vehPrecio = precio
            db.session.commit()
            flash('Datos actualizados correctamente', 'success')
            return redirect("/cliente/"+tipo+"/VehiculosReg")
        else:
            updateVehiculo.datId = datoId
            updateVehiculo.cateId = cateId
            updateVehiculo.vehModelo = modelo
            updateVehiculo.vehMarca = marca
            updateVehiculo.vehEstado = estado
            updateVehiculo.vehPrecio = precio
            db.session.commit()
            flash('Datos actualizados correctamente', 'success')
            return redirect("/cliente/"+tipo+"/VehiculosReg")
        

    datosVehiculos = db.session.query(Vehiculo,Categoria,DatosPersonales).outerjoin(Categoria,DatosPersonales).all()
    datosCategorias = Categoria.query.all()
    datosUsuario = DatosPersonales.query.all()
    
    usuarioRol = Usuario_Rol.query.filter(Usuario_Rol.usuId == current_user.usuId).all()
    rolesUsuarioList =  []
    for x in usuarioRol:
        rolesUsuario = Rol.query.filter(Rol.rolId == x.rolId).first()
        rolesUsuarioList.append(rolesUsuario.rolTipo)

    if tipo in rolesUsuarioList:

        context = {
            'datosUsuarios' : datosUsuario,
            'listaCategorias' : datosCategorias,
            'listaVehiculos' : datosVehiculos,
            'rolesUsuario'  : rolesUsuarioList,
            'usuarioActual' : current_user,
            'activeRol' : tipo
        }

        return render_template('paginaCliente.html', **context, usuarioId = str(current_user.usuId))
    else:
        flash('No tienes este rol', 'error')
        return redirect(url_for('paginaCliente'))

@app.route('/cliente/<tipo>/catalogo', methods=['GET', 'POST'])
@login_required
def catalogoVehiculos(tipo):

    datosVehiculos = db.session.query(Vehiculo,Categoria,DatosPersonales).outerjoin(Categoria,DatosPersonales).filter(Vehiculo.datId == None).all()
    datosCategorias = Categoria.query.all()
    datosUsuario = DatosPersonales.query.all()
    
    usuarioRol = Usuario_Rol.query.filter(Usuario_Rol.usuId == current_user.usuId).all()
    rolesUsuarioList =  []
    for x in usuarioRol:
        rolesUsuario = Rol.query.filter(Rol.rolId == x.rolId).first()
        rolesUsuarioList.append(rolesUsuario.rolTipo)

    if tipo in rolesUsuarioList:

        context = {
            'datosUsuarios' : datosUsuario,
            'listaCategorias' : datosCategorias,
            'listaVehiculos' : datosVehiculos,
            'rolesUsuario'  : rolesUsuarioList,
            'usuarioActual' : current_user,
            'activeRol' : tipo
        }

        return render_template('paginaCliente.html', **context, usuarioId = str(current_user.usuId))
    else:
        flash('No tienes este rol', 'error')
        return redirect(url_for('paginaCliente'))


@app.route('/cliente/<tipo>/editarPerfil/<userId>', methods=['GET', 'POST'])
@login_required
def editarPerfil(tipo,userId):

    if request.method == 'POST':
        nombre = request.form['datNombre']
        apellido = request.form['datApellido']
        telefono = request.form['datTelefono']
        correo = request.form['datCorreo']
        
        datosPerfilUsuario = DatosPersonales.query.filter(DatosPersonales.usuId == userId).first()
        datosPerfilUsuario.datNombre = nombre
        datosPerfilUsuario.datApellido = apellido
        datosPerfilUsuario.datTelefono = telefono
        datosPerfilUsuario.datCorreo = correo

        db.session.add(datosPerfilUsuario)
        db.session.commit()

        flash('Datos actualizados correctamente', 'success')
        return redirect("/cliente/"+tipo+"/editarPerfil/"+userId) 


    datosUsuario = DatosPersonales.query.filter(DatosPersonales.datId == current_user.usuId).first()
    datosUsuList = []
    datosUsuList.append(datosUsuario)

    usuarioRol = Usuario_Rol.query.filter(Usuario_Rol.usuId == current_user.usuId).all()
    rolesUsuarioList =  []
    for x in usuarioRol:
        rolesUsuario = Rol.query.filter(Rol.rolId == x.rolId).first()
        rolesUsuarioList.append(rolesUsuario.rolTipo)

    if tipo in rolesUsuarioList:

        context = {
            'datosPersonales' : datosUsuList,
            'rolesUsuario'  : rolesUsuarioList,
            'usuarioActual' : current_user,
            'activeRol' : tipo
        }


        return render_template('perfilCliente.html', **context, usuarioId = str(current_user.usuId))

    else:
        flash('No tienes este rol', 'error')
        return redirect(url_for('paginaCliente'))


@app.route('/cliente/report/pdf')
@login_required
def download_report():

    datosUsuario = DatosPersonales.query.filter(DatosPersonales.datId == current_user.usuId).all()
    vehiculosList =  []
    for x in datosUsuario:
        vehiculoUsuario = Vehiculo.query.filter(Vehiculo.datId == x.datId).first()
        vehiculosList.append(vehiculoUsuario)
    
    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width/6
        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Reporte vehiculos comprados', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)
    pdf.cell(col_width, pdf.font_size, 'Placa', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Modelo', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Marca', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Estado', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Precio', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Categoria',border=1, ln=0, align='C', fill=0)
        
    pdf.ln(4)
        
    th = pdf.font_size
    pdf.set_font('Courier', '', 12)
    for row in vehiculosList:
        pdf.cell(col_width, th, str(row.vehPlaca), border=1, ln=0, align='C')
        pdf.cell(col_width, th, str(row.vehModelo), border=1, ln=0, align='C')
        pdf.cell(col_width, th, row.vehMarca, border=1, ln=0, align='C')
        pdf.cell(col_width, th, row.vehEstado, border=1, ln=0, align='C')
        pdf.cell(col_width, th, str(row.vehPrecio), border=1, ln=0, align='C')
        pdf.cell(col_width, th, str(row.catId), border=1, ln=0, align='C')
        pdf.ln(th)
        
    pdf.ln(10)
        
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- Fin reporte -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=vehicle_report.pdf'})

@app.route('/vendedor/report/pdf')
@login_required
def download_report_vendedor():

    datosVehiculos = db.session.query(Vehiculo,Categoria,DatosPersonales).join(Categoria,DatosPersonales).all()
    
    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width/8
        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Reporte vehiculos', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)
    pdf.cell(col_width, pdf.font_size, 'Placa', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Modelo', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Marca', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Estado', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Precio', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Nombre', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Apellido', border=1, ln=0, align='C', fill=0)
    pdf.cell(col_width, pdf.font_size, 'Categoria',border=1, ln=0, align='C', fill=0)
        
    pdf.ln(4)
        
    th = pdf.font_size
    pdf.set_font('Courier', '', 12)
    for row, row2, row3 in datosVehiculos:
        pdf.cell(col_width, th, str(row.vehPlaca), border=1, ln=0, align='C')
        pdf.cell(col_width, th, str(row.vehModelo), border=1, ln=0, align='C')
        pdf.cell(col_width, th, row.vehMarca, border=1, ln=0, align='C')
        pdf.cell(col_width, th, row.vehEstado, border=1, ln=0, align='C')
        pdf.cell(col_width, th, str(row.vehPrecio), border=1, ln=0, align='C')
        pdf.cell(col_width, th, row3.datNombre, border=1, ln=0, align='C')
        pdf.cell(col_width, th, row3.datApellido, border=1, ln=0, align='C')
        pdf.cell(col_width, th, str(row2.catTipo), border=1, ln=0, align='C')
        pdf.ln(th)
        
    pdf.ln(10)
        
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- Fin reporte -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=vendedor_report.pdf'})


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

