# Flask con Películas — Guía para Estudiantes

Vamos a aprender Flask desde cero. Primero los fundamentos, después 15 retos con datos de películas.

---

## 1. Fundamentos

### ¿Qué es Flask?

Flask es un **framework web** para Python. "Framework web" significa que nos da las herramientas para crear aplicaciones que hablan HTTP — el lenguaje que entienden los navegadores.

Cuando escribís una app con Flask, estás creando un **backend**: un programa que corre en un servidor (tu compu mientras desarrollas), escucha peticiones y **siempre devuelve una respuesta**.

### ¿Cómo funciona? (Cliente → Servidor → Respuesta)

```
Navegador (cliente)          Flask (servidor)
       │                           │
       │── GET /peliculas ────────>│
       │                           │── busca películas
       │                           │── arma la respuesta
       │<── [lista de películas] ──│
```

Cada vez que un cliente (navegador, Postman, otra app) hace una petición a nuestro servidor:

1. Flask recibe la petición
2. Busca la ruta que coincide
3. Ejecuta la función asociada
4. La función **devuelve** una respuesta
5. Flask envía esa respuesta al cliente

**Regla de oro del backend:** toda función de ruta TIENE que devolver algo. 

### ¿Qué puedo devolver?

| Tipo | Ejemplo | Lo que llega al cliente |
|------|---------|------------------------|
| `dict` | `{"id": 1, "titulo": "The Matrix"}` | JSON |
| `list` | `["a", "b", "c"]` | JSON |
| `str` | `"Hola"` | Texto plano |
| `tuple` | `(datos, 404)` | JSON + código HTTP |
| `int` | `404` | Texto + código HTTP (como fallback) |



### ¿Qué es una ruta?

Una **ruta** (o endpoint) es una URL que nuestra app entiende. Cuando alguien visita `http://localhost:5000/peliculas`, Flask busca una función que maneje esa ruta y ejecuta el código.

### ¿Cómo creo una ruta?

Usamos un **decorador** `@app.route()`:

```python
@app.route("/peliculas")
def listar_peliculas():
    return ["una", "lista", "de", "datos"]
```

El decorador le dice a Flask: "cuando alguien visite `/peliculas`, ejecutá esta función". El `return` de la función es lo que se envía como respuesta.

### ¿Cómo paso parámetros en la ruta?

**Opción 1 — Parte de la ruta (path param):**

```python
@app.route("/peliculas/<int:id>")
def pelicula_por_id(id):
    return f"El ID recibido es {id}"
```

Usamos `<int:id>` para capturar un valor de la URL. El `int:` convierte automáticamente a número entero.

**Opción 2 — Query params (después del `?`):**

Cuando ves `?genero=Acción&rating_min=9` en la URL, eso son query params. Se leen con `request.args`:

```python
from flask import request

@app.route("/peliculas")
def listar():
    genero = request.args.get("genero")
    rating_min = request.args.get("rating_min", type=float)
    return f"Filtrando por {genero} con rating mínimo {rating_min}"
```

Siempre importamos `request` al principio del archivo: `from flask import Flask, request`.

### ¿Por qué `type=float`?

Todo lo que viene en la URL es texto. `?rating_min=9` llega como el string `"9"`, no el número `9`. Si hacemos `>=` con strings, falla. `type=float` le dice a Flask que lo convierta automáticamente.

### Formato de las respuestas

Cuando devolvés un `dict` o una `list`, Flask lo convierte automáticamente a JSON:

```python
return {"mensaje": "Hola"}         # → JSON
return [1, 2, 3]                   # → JSON

# Para errores, devolvemos (cuerpo, código_http)
return {"error": "No encontrada"}, 404
```

---

## 2. Setup

```bash
pip install flask
```

Creá un archivo `app.py` con esta base:

```python
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

if __name__ == '__main__':
    app.run(debug=True)
```

Corré con:

```bash
python app.py
```

---

## 3. Retos

### Nivel 1 — Rutas básicas

**R1** `GET /peliculas` → devolvé todas las películas.

**R2** `GET /peliculas/<id>` → devolvé UNA película por su ID. Si no existe, devolvé `{"error": "No encontrada"}` con código 404.

**R3** `GET /peliculas/<id>/creditos` → devolvé solo el título y director de la película con ese ID.

---

### Nivel 2 — Filtrar con query params

> Todos los retos de este nivel modifican la ruta `GET /peliculas`. Cada vez agregás un filtro nuevo.

**R4** `GET /peliculas?genero=Drama` → devolvé solo las películas de ese género. Tiene que funcionar aunque escriban "drama" o "DRAMA" (case-insensitive).

**R5** `GET /peliculas?rating_min=9` → devolvé solo películas con rating >= 9.

**R6** `GET /peliculas?año=1994` → devolvé solo las del año 1994.

**R7** `GET /peliculas?genero=Drama&rating_min=8.5` → combiná filtros. Tienen que cumplirse TODOS a la vez.

---

### Nivel 3 — Transformar datos

**R8** `GET /peliculas/titulos` → devolvé solo una lista de títulos:

```json
["The Shawshank Redemption", "The Godfather", "The Dark Knight", ...]
```

**R9** `GET /peliculas/resumen` → devolvé una lista de resúmenes:

```json
[
  "The Shawshank Redemption (1994) - Dir. Frank Darabont",
  "The Godfather (1972) - Dir. Francis Ford Coppola",
  ...
]
```

**R10** `GET /peliculas/agrupadas` → devolvé las películas agrupadas por género:

```json
{
  "Drama": [ ... ],
  "Acción": [ ... ],
  "Crimen": [ ... ],
  "Ciencia Ficción": [ ... ]
}
```

**R11** `GET /peliculas/estadisticas` → devolvé:

```json
{
  "total": 10,
  "rating_promedio": 8.82,
  "generos": 4,
  "pelicula_mejor_rating": "The Shawshank Redemption",
  "año_mas_antiguo": 1972,
  "año_mas_nuevo": 2019
}
```

---

### Nivel 4 — Ordenar y topes

**R12** `GET /peliculas?ordenar_por=rating&orden=desc` → ordená las películas por rating. El parámetro `orden` puede ser `asc` o `desc` (por defecto `asc`). También funciona con `?ordenar_por=año&orden=asc`.

**R13** `GET /peliculas/top?limite=3` → devolvé las 3 películas con mejor rating (o las que indique `limite`).

---

### Nivel 5 — Búsqueda

**R14** `GET /peliculas/buscar?q=dark` → buscá películas cuyo título CONTENGA el texto (case-insensitive). "dark" debería encontrar "The Dark Knight".

**R15** `GET /peliculas/buscar?q=nolan` → ahora buscá también por director. Si coincide con título O director, devolvela.

---

## 4. Tips útiles

```python
# Recorrer lista y armar resultado
resultado = []
for p in PELICULAS:
    if p["genero"] == genero:
        resultado.append(p)

# Case-insensitive
if texto.lower() in p["titulo"].lower():

# Obtener query params
genero = request.args.get("genero")
rating_min = request.args.get("rating_min", type=float)

# Ordenar lista de diccionarios por una clave
def obtener_rating(pelicula):
    return pelicula["rating"]

ordenadas = sorted(PELICULAS, key=obtener_rating, reverse=True)

# Tomar los primeros N
top = ordenadas[:limite]

# Error 404
return {"error": "No encontrada"}, 404
```

---

## 5. Checklist

- [ ] R1 a R3 — sé usar rutas con `<int:id>`
- [ ] R4 a R7 — sé leer query params con `request.args.get()`
- [ ] R8 a R11 — sé transformar listas con `for` y `append()`
- [ ] R12, R13 — sé ordenar con `sorted()` y tomar los primeros N
- [ ] R14, R15 — sé buscar texto con `in`
- [ ] Probé cada endpoint con el navegador
