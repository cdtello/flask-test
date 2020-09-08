from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask import Flask


app = Flask(__name__)

app.secret_key = 'clave_secreta_flask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/proyectoflask?charset=utf8'
db = SQLAlchemy(app)

# Conexion DB
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'proyectoflask'

# mysql = MySQL(app)
from controller import *

if __name__ == '__main__':
    app.run(debug=True)
