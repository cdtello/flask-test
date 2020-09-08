from main import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    telefono = db.Column(db.String(50))  
    foto = db.Column(db.String(50))
    facturas = db.relationship('Factura', backref='cliente')

    def __repr__(self):
        return '<Nombre %r>' % self.nombre

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    nombre = db.Column(db.String(50))
    precio = db.Column(db.Integer, default=0)  
    cantidad_bodega = db.Column(db.Integer, default=0) 
    estado = db.Column(db.Integer, default=0) 

    def __repr__(self):
        return '<Nombre %r>' % self.nombre

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)
    productos = db.relationship('Producto', backref='cat')

    def __repr__(self):
        return '<Nombre %r>' % self.nombre

products_fac = db.Table('products_fac',
    db.Column('factura_id', db.Integer, db.ForeignKey('factura.id')),
    db.Column('producto_id', db.Integer, db.ForeignKey('producto.id'))
    )

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    productos = db.relationship('Producto', secondary=products_fac, backref = db.backref('productosfacturados', lazy='dynamic'))
    cantidad_productos = db.Column(db.Integer, default=0) 
    valor_total = db.Column(db.Integer, default=0)  
    metodo_pago = db.Column(db.String(50)) 

    def __repr__(self):
        return '<Nombre %r>' % self.nombre


