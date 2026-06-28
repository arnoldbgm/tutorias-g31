from flask import Flask
from db import db
from flask_migrate import Migrate
from flask_restful import Api
from flask_mail import Mail
from models import usuarios
from resources.usuariosResource import UsuariosResource

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'arnold.gallegosm@gmail.com'
app.config['MAIL_PASSWORD'] = 'mwdh atnx yjdc vuid'
app.config['MAIL_DEFAULT_SENDER'] = 'arnold.gallegosm@gmail.com'
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