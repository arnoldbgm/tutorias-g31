from flask import Flask, request

app = Flask(__name__)

PELICULAS = [
    {"id": 1, "titulo": "The Shawshank Redemption", "año": 1994, "genero": "Drama", "rating": 9.3, "director": "Frank Darabont"},
    {"id": 2, "titulo": "The Godfather", "año": 1972, "genero": "Crimen", "rating": 9.2, "director": "Francis Ford Coppola"},
    {"id": 3, "titulo": "The Dark Knight", "año": 2008, "genero": "Acción", "rating": 9.0, "director": "Christopher Nolan"},
    {"id": 4, "titulo": "Pulp Fiction", "año": 1994, "genero": "Crimen", "rating": 8.9, "director": "Quentin Tarantino"},
    {"id": 5, "titulo": "Schindler's List", "año": 1993, "genero": "Drama", "rating": 9.0, "director": "Steven Spielberg"},
    {"id": 6, "titulo": "Forrest Gump", "año": 1994, "genero": "Drama", "rating": 8.8, "director": "Robert Zemeckis"},
    {"id": 7, "titulo": "The Matrix", "año": 1999, "genero": "Acción", "rating": 8.7, "director": "Lana Wachowski"},
    {"id": 8, "titulo": "Interstellar", "año": 2014, "genero": "Ciencia Ficción", "rating": 8.7, "director": "Christopher Nolan"},
    {"id": 9, "titulo": "Parasite", "año": 2019, "genero": "Drama", "rating": 8.5, "director": "Bong Joon-ho"},
    {"id": 10, "titulo": "Mad Max: Fury Road", "año": 2015, "genero": "Acción", "rating": 8.1, "director": "George Miller"},
]

# Retos de rutas
# Estamos trabajando en Netflix y nos piden que devolamos
# la siguiente informacion

# Para crear una ruta siempre usamos la siguiente sintaxis
# @app.route("")
# Siempre debajo de una ruta debe de encontrarse una funcion
@app.route("/peliculas")
def listar_peliculas():
   return PELICULAS

#  [1,2,3,4,5,6]  Arreglo - Python Lista

@app.route("/peliculas/<int:id>")
def listar_una_pelicula(id):
   # Vamos a recorrer el arreglo
   for elmt in PELICULAS:
      if elmt["id"] == id:
         return elmt
   return {
       "error": "No encontramos la pelicula"
   }

@app.route("/peliculas/<int:id>/creditos")
def listar_una_pelicula_creditos(id):
   for elmt in PELICULAS:
      if elmt["id"] == id:
         # {"id": 8, 
         # "titulo": "Interstellar", 
         # "año": 2014, 
         # "genero": "Ciencia Ficción",
         # "rating": 8.7,
         # "director": "Christopher Nolan"},
         return {
            "titulo": elmt["titulo"],
            "director": elmt["director"]
         }   
      
# Vamos a crear ahora un endpoint
# /pelicula?genero=Drama
@app.route("/pelicula")
def listar_peliculas_genero():
   genero = request.args.get("genero") # Drama
   rating_min = request.args.get("rating_min", type=float) # Rating minimo

   # Cambio del nombre de la varible
   resultado = PELICULAS

   # Para trabajar con los queryparams
   if genero:
      resulto_filtrado = []
      for elmt in resultado:
         if elmt["genero"].lower() == genero.lower():
            resulto_filtrado.append(elmt)
      # Ahora haremos que mi resultado filtrado sea mis resultado
      resultado = resulto_filtrado

   if rating_min is not None:
      resulto_filtrado = []
      for elmt in resultado:
         if elmt["rating"] >= rating_min:
            resulto_filtrado.append(elmt)
      resultado = resulto_filtrado

   return resultado

@app.route("/peliculas/agrupadas")
def peliculas_agrupadas():
   grupos = {}
   for p in PELICULAS:
      genero = p["genero"]

      # Creacion de las keys de mi diccionario
      if genero not in grupos:
         grupos[genero] = []

      grupos[genero].append(p)

   return grupos


if __name__ == '__main__':
    app.run(debug=True, port=8081)