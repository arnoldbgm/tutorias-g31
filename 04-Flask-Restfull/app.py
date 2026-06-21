# Dentro del archivo app.py
# Vamos a crear y configurar nuestro servidor
# en Flask

from flask import Flask
from db import db
from flask_migrate import Migrate
from flask_restful import Api
from models import categoria, post # Importacion de tus tablas
from resources.categoria_resource import CategoriasListResource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://neondb_owner:npg_BGEC5YV8oIbS@ep-withered-rain-acxpdk1t-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

db.init_app(app)

migrate = Migrate(app, db) # Ya esta configurado las migraciones

api = Api(app) # Convierte nuestro servidor en una API REST

# Creacion de mis rutas
api.add_resource(CategoriasListResource, "/categorias")

if __name__ == '__main__':
   app.run(debug=True)