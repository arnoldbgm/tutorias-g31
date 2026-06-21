from flask_restful import Resource
from flask import request  
from models.categoria import CategoriasTable
from db import db

class CategoriasListResource(Resource):

   def post(self):
      # Un POST funciona de la siguiente forma
      # 1- Un usuario envia informacion en formato json
      #    Debo capturar esa informacion ✅
      # 2- Debo crear un formato para insertarlo en nuestra
      #    tabla ✅
      # 3- Debemos de insertar el elemento y cortar la conexion ✅
      # 4- Siempre debemos responder o retonar informacion ✅
      data = request.get_json()
      #{
      #  nombre: "Electronica"
      #}
      nueva_categoria = CategoriasTable(nombre=data['nombre'])

      db.session.add(nueva_categoria)
      db.session.commit()

      return{
         'msg': "Exito al insertar el registro",
         'id': nueva_categoria.id,
         'nombre': nueva_categoria.nombre
      }, 201