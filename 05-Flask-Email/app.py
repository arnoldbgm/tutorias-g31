from flask import Flask
from db import db
from flask_migrate import Migrate
from flask_restful import Api
from flask_mail import Mail
from models import usuarios
from resources.usuariosResource import UsuariosResource
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db.init_app(app)
migrate = Migrate(app,db)
api = Api(app)
mail = Mail(app)

# Rutas de mi aplicacion
api.add_resource(UsuariosResource, '/usuarios/registro')


if __name__ == '__main__':
   app.run(debug=True)