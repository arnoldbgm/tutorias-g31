from flask import request, jsonify
from flask_restful import Resource
from models.usuarios import UsuariosTable
from db import db
from utils.email_utils import enviar_correo

class UsuariosResource(Resource):
   # El registro de usuarios siempre es del tipo POST

   def post(self):
      # Solicitar al usuario que envie la informacion
      # para crear su usuario
      # {
      #    nombre: "Arnold",
      #    telefono: "920224310",
      #    correo: "arnold.gallegos@ucsp.edu.pe",
      #    password: "123456"
      # }
      data = request.get_json()

      nuevo_usuario = UsuariosTable(**data)

      # Guardar el nuevo usuario en la bd
      db.session.add(nuevo_usuario)
      db.session.commit()

      # Enviar el correo de bienvenida
      enviar_correo(nuevo_usuario.correo, nuevo_usuario.nombre)

      # Entregar la respuesta
      return jsonify({
         'msg': 'Correo enviado'
      })