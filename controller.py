from flask import Flask, redirect, url_for, render_template, request, flash, current_app
from main import app
from models import *
from datetime import datetime
from werkzeug.utils import secure_filename
import secrets
import os


# Context processors
# @app.context_processor
# def date_now():
#     return{
#         'now': datetime.now()
#     }

# Endpoints


@app.route('/')
def index():
    return render_template('index.html')

def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/images', photo_name)
    photo.save(file_path)
    return photo_name

# *********************************************** CRUD CLIENTE ****************************************************
@app.route('/crear_cliente', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':

        cedula = request.form['cedula']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        foto = request.files['foto']

        foto = save_images(foto)

        
        cliente = Cliente.query.filter_by(cedula = cedula).first()
        if cliente:
                flash('El cliente con la cedula '+ cedula + ' ya existe en la BD')
                return redirect(url_for('crear_cliente'))
        else:
            try:
                cliente = Cliente(cedula = cedula, nombre = nombre, direccion = direccion, telefono = telefono, foto = foto)
                db.session.add(cliente)
                db.session.commit()
                flash('Has creado el coche correctamente!!')
                return redirect(url_for('clientes'))
            except:
                flash('Error de creación!!')
            return redirect(url_for('crear_cliente'))

        # cursor = mysql.connection.cursor()
        # cursor.execute("INSERT INTO coches VALUES (NULL, %s, %s, %s, %s)", (marca, modelo, precio, ciudad))
        # cursor.connection.commit()
    return render_template('cliente_templates/crear_cliente.html')

@app.route('/clientes')
def clientes():

    clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM coches ORDER BY id DESC')
    # coches = cursor.fetchall()
    # cursor.close()
    return render_template('cliente_templates/clientes.html', clientes = clientes)

@app.route('/cliente/<cliente_id>')
def cliente(cliente_id):
    # cursor = mysql.connection.cursor()
    # cursor.execute("SELECT * FROM coches WHERE id = %s",(cliente_id))
    # coche = cursor.fetchall()
    # cursor.close()
    cliente = Cliente.query.filter_by(id = cliente_id).first()
    return render_template('cliente_templates/cliente.html', cliente = cliente)

@app.route('/borrar_cliente/<cliente_id>')
def borrar_cliente(cliente_id):
    cliente = Cliente.query.filter_by(id = int(cliente_id)).first()
    cliente.delete()
    db.session.commit()
    # cursor = mysql.connection.cursor()
    # cursor.execute("DELETE FROM coches WHERE id = %s",(cliente_id))
    # mysql.connection.commit()
    flash('El Cliente ha sido eliminado')
    return redirect(url_for('clientes'))

@app.route('/editar_cliente/<cliente_id>', methods=['GET','POST'])
def editar_cliente(cliente_id):

    cliente = Cliente.query.filter_by(id = int(cliente_id)).first()
    
    if request.method == 'POST':
    
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        foto = request.files['foto']

        foto = save_images(foto)

        cliente = Cliente.query.filter_by(id = int(cliente_id)).first()
        cliente.cedula = cedula
        cliente.nombre = nombre
        cliente.direccion = direccion
        cliente.telefono = telefono
        cliente.foto = foto

        db.session.commit()
        # cursor = mysql.connection.cursor()
        # cursor.execute("""
        #     UPDATE coches
        #     SET marca = %s,
        #         modelo = %s,
        #         precio = %s,
        #         ciudad = %s
        #     WHERE id = %s
        # """, (marca, modelo, precio, ciudad, coche_id))
        # cursor.connection.commit()
        flash('Has editado el cliente correctamente!!')
        return redirect(url_for('clientes'))

    # cursor = mysql.connection.cursor()
    # cursor.execute("SELECT * FROM coches WHERE id = %s",(coche_id))
    # coche = cursor.fetchall()
    # cursor.close()
    return render_template('cliente_templates/crear_cliente.html', cliente = cliente)

# *********************************************** FIN CRUD CLIENTE ****************************************************

# *********************************************** CRUD PRODUCTO ****************************************************
@app.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':

        codigo = request.form['codigo']
        categoria_id = request.form['categoria']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad_bodega = request.form['cantidad']
        try:
            estado = request.form['estado']
            estado = 1
        except:
            estado = 0

        print("*** Mostrando Estado ***")
        print(estado)
   
        producto = Producto.query.filter_by(codigo = codigo).first()
        if producto:
                flash('El producto con el codigo '+ codigo + ' ya existe en la BD')
                return redirect(url_for('crear_producto'))
        else:
            try:
                producto = Producto(codigo = codigo, categoria_id = categoria_id, nombre = nombre, precio = precio, cantidad_bodega = cantidad_bodega, estado = estado)
                db.session.add(producto)
                db.session.commit()
                flash('Has creado el producto correctamente!!')
                return redirect(url_for('productos'))
            except:
                flash('Error de creación!!')
            return redirect(url_for('crear_producto'))
    categorias = Categoria.query.all()
    return render_template('producto_templates/crear_producto.html', categorias = categorias)

@app.route('/productos')
def productos():

    productos = Producto.query.order_by(Producto.id.desc()).all()

    return render_template('producto_templates/productos.html', productos = productos)

@app.route('/producto/<producto_id>')
def producto(producto_id):

    producto = Producto.query.filter_by(id = producto_id).first()
    categoria = Categoria.query.filter_by(id = producto.categoria_id).first()
    return render_template('producto_templates/producto.html', producto = producto, categoria = categoria)

@app.route('/borrar_producto/<producto_id>')
def borrar_producto(producto_id):
    producto = Producto.query.filter_by(id = int(producto_id)).first()
    producto.delete()
    db.session.commit()
    flash('El Producto ha sido eliminado')
    return redirect(url_for('productos'))

@app.route('/editar_producto/<producto_id>', methods=['GET','POST'])
def editar_producto(producto_id):

    producto = Producto.query.filter_by(id = int(producto_id)).first()
    
    if request.method == 'POST':
    
        codigo = request.form['codigo']
        categoria_id = request.form['categoria']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad_bodega = request.form['cantidad']
        try:
            estado = request.form['estado']
            estado = 1
        except:
            estado = 0

        producto = Producto.query.filter_by(id = int(producto_id)).first()
        producto.codigo = codigo
        producto.categoria_id = categoria_id
        producto.nombre = nombre
        producto.precio = precio
        producto.cantidad_bodega = cantidad_bodega
        producto.estado = estado

        db.session.commit()
        flash('Has editado el Producto correctamente!!')
        return redirect(url_for('productos'))
    categorias = Categoria.query.all()
    return render_template('producto_templates/crear_producto.html', producto = producto, categorias = categorias)

# *********************************************** FIN CRUD PRODUCTO ****************************************************
# *********************************************** CRUD CATEGORIA ****************************************************
@app.route('/crear_categoria', methods=['GET', 'POST'])
def crear_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']

        categoria = Categoria.query.filter_by(nombre = nombre).first()
        if categoria:
                flash('La Categoria '+ nombre + ' ya existe en la BD')
                return redirect(url_for('crear_categoria'))
        else:
            try:
                categoria = Categoria(nombre = nombre)
                db.session.add(categoria)
                db.session.commit()
                flash('Has creado la Categoria correctamente!!')
                return redirect(url_for('categorias'))
            except:
                flash('Error de creación!!')
            return redirect(url_for('crear_categoria'))

    return render_template('categoria_templates/crear_categoria.html')

@app.route('/categorias')
def categorias():

    categorias = Categoria.query.order_by(Categoria.id.desc()).all()

    return render_template('categoria_templates/categorias.html', categorias = categorias)

@app.route('/categoria/<categoria_id>')
def categoria(categoria_id):

    categoria = Categoria.query.filter_by(id = categoria_id).first()
    return render_template('categoria_templates/categoria.html', categoria = categoria)

@app.route('/borrar_categoria/<categoria_id>')
def borrar_categoria(categoria_id):
    categoria = Categoria.query.filter_by(id = int(categoria_id)).first()
    categoria.delete()
    db.session.commit()
    flash('La Categoria ha sido eliminada')
    return redirect(url_for('categorias'))

@app.route('/editar_categoria/<categoria_id>', methods=['GET','POST'])
def editar_categoria(categoria_id):

    categoria = Categoria.query.filter_by(id = int(categoria_id)).first()
    
    if request.method == 'POST':
        nombre = request.form['nombre']


        categoria = Categoria.query.filter_by(id = int(categoria_id)).first()
        categoria.nombre = nombre

        db.session.commit()
        flash('Has editado la Categoria correctamente!!')
        return redirect(url_for('categorias'))

    return render_template('categoria_templates/crear_categoria.html', categoria = categoria)

# *********************************************** FIN CRUD CATEGORIA ****************************************************

# *********************************************** CRUD FACTURAS ****************************************************
@app.route('/crear_factura', methods=['GET', 'POST'])
def crear_factura():
    if request.method == 'POST':

        cliente_id = request.form['cedula']
        productos = request.form.getlist('productos')
        metodo_pago = request.form['metodopago']

        cantidad_productos = len(productos) 
        valor_total = 0

        # try:
        cliente = Cliente.query.filter_by(cedula = cliente_id).first()
        factura = Factura(cliente_id = cliente.id, metodo_pago = metodo_pago, cantidad_productos=cantidad_productos)
        
        for pro in productos:
            pro = Producto.query.filter_by(id = pro).first()
            valor_total = valor_total + pro.precio
            pro.productosfacturados.append(factura)
        
        factura.valor_total = valor_total
        
        db.session.add(factura)
        db.session.commit()

        flash('Has creado la factura correctamente!!')
        return redirect(url_for('facturas'))
        # except:
        #     flash('Error de creación!!')
        # return redirect(url_for('crear_factura'))
    productos = Producto.query.all()
    return render_template('factura_templates/crear_factura.html', productos = productos)

@app.route('/facturas')
def facturas():

    facturas = Factura.query.order_by(Factura.id.desc()).all()
    
    return render_template('factura_templates/facturas.html', facturas = facturas)

@app.route('/factura/<factura_id>')
def factura(factura_id):

    factura = Factura.query.filter_by(id = factura_id).first()
    print("*** mostrando productos ***")
    print(factura.productos)
    cliente = Cliente.query.filter_by(id = factura.cliente_id).first()
    return render_template('factura_templates/factura.html', factura = factura, cliente = cliente)

@app.route('/borrar_factura/<factura_id>')
def borrar_factura(factura_id):
    factura = Factura.query.filter_by(id = int(factura_id)).first()
    factura.delete()
    db.session.commit()
    flash('La Factura ha sido eliminado')
    return redirect(url_for('facturas'))

@app.route('/editar_factura/<factura_id>', methods=['GET','POST'])
def editar_factura(factura_id):

    factura = Factura.query.filter_by(id = int(factura_id)).first()
    
    if request.method == 'POST':
    
        codigo = request.form['codigo']
        cliente_id = request.form['cliente']
        productos = request.form['productos']
        cantidad_productos = total_productos
        valor_total = valor_total
        metodo_pago = request.form['metodopago']


        factura = Producto.query.filter_by(id = int(factura_id)).first()
        factura.codigo = codigo
        factura.cliente_id = cliente_id

        db.session.commit()
        flash('Has editado la Factura correctamente!!')
        return redirect(url_for('facturas'))
    categorias = Categoria.query.all()
    return render_template('factura_templates/crear_factura.html', factura = factura)

# *********************************************** API ****************************************************

@app.route('/api_factura/<factura_id>')
def api_factura(factura_id):
    factura = Factura.query.filter_by(id = int(factura_id)).first()
    return "Valor total: $"+str(factura.valor_total)


# *********************************************** CIFRADO ****************************************************

@app.route('/api_cifrado/<mensaje>/<desplazamiento>')
def api_cifrado(mensaje,desplazamiento):
    mensaje = mensaje.upper()
    salida = ""
    desplazamiento = int(desplazamiento)
    for m in mensaje:
        mconv = ord(m) + desplazamiento
        if mconv > 90:
            mconv = mconv - 90 + 64
        salida = salida + chr(mconv)
        
    mensaje = mensaje
    return "Mensaje: "+ salida