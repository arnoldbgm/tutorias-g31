from flask import Flask, jsonify
from db import create_tables, get_db_conection

app = Flask(__name__)

# Apenas se cree mi servidor
# quiero que se creen mis tablas
create_tables()

# Vamos a crear un endpoint para devolver todas
# las categorias que tengo en mi base de datos
@app.route('/categorias')
def categorias():
   # Yo quiero listar o devolver todas las 
   # categorias de la bd
   # conexion con la bd
   conn = get_db_conection()
   categorias = [] # Vamos a dar formato
   with conn:
      with conn.cursor() as cursor:
         # Es que estoy conectandome y vamos a pasar a ejecutar codigo SQL
         cursor.execute('SELECT * FROM categorias')
         # Con un cursor debo establecer con cuanta informacion me quedo
         rows = cursor.fetchall()       
         # 🏅 Siempre debemos devolver informacion
         # SIEMPRE SE DEBE return algo

         # La informacion llega asi 
         #  (1, 'Electrónica', 'Dispositivos electrónicos y accesorios', datetime.datetime(2026, 6, 15, 1, 19, 1, 761548))
         #  (2, 'Ropa', 'Prendas de vestir para toda la temporada', datetime.datetime(2026, 6, 15, 1, 19, 1, 761548))
         #  (3, 'Hogar', 'Artículos para el hogar y decoración', datetime.datetime(2026, 6, 15, 1, 19, 1, 761548))   
         for row in rows:
            # Todos estos elementos vamos a insertarlos dentro de nuestro
            # lista llamada categorias
            categorias.append({
               'id': row[0],
               'nombre': row[1],
               'descripcion': row[2],
               'created_at': str(row[3])
            })
   
   return jsonify(categorias)

if __name__ == "__main__":
   app.run(debug=True)