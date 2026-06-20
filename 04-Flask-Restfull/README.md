# 📌 Guía: API REST con Flask-RESTful, SQLAlchemy, Flask-Migrate y PostgreSQL

En esta guía, crearemos una API REST en **Flask** utilizando **Flask-RESTful**, donde **toda la lógica vive dentro de Resources**, siguiendo el estándar oficial.

---

# 📂 **Estructura del Proyecto**

```bash
/project_root
├── app.py                # Inicialización de la app y rutas
├── db.py                 # Configuración de SQLAlchemy
├── models/               # Modelos de base de datos
│   ├── __init__.py
│   ├── categoria.py
│   └── post.py
├── resources/            # ✅ Resources (ANTES controllers + routes)
│   ├── __init__.py
│   ├── categoria_resource.py
│   └── post_resource.py
├── migrations/           # Migraciones de la BD
└── requirements.txt
```

📌 **IMPORTANTE:**

* ❌ Eliminamos `controllers/`
* ❌ Eliminamos `routes/`
* ✅ Usamos solo `resources/` (estándar Flask-RESTful)

---

# 1️⃣ **Crear entorno virtual e instalar dependencias**

```bash
python -m venv venv
```

### Activar:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Instalar dependencias:

```bash
pip install flask flask-restful flask-sqlalchemy flask-migrate psycopg2-binary
```

### requirements.txt

```
flask
flask-restful
flask-sqlalchemy
flask-migrate
psycopg2
```

```bash
pip install -r requirements.txt
```

---

# 2️⃣ **Configurar la base de datos (`db.py`)**

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

---

# 3️⃣ **Crear los Modelos (`models/`)**

## 📌 `models/categoria.py`

```python
from db import db
from sqlalchemy import Column, Integer, String

class CategoriasTable(db.Model):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
```

---

## 📌 `models/post.py`

```python
from db import db
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

class PostTable(db.Model):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
```
---

# **Migraciones con Flask-Migrate**

```bash
flask db init
flask db migrate -m "Inicial"
flask db upgrade
```


---

# 4️⃣ **Crear los Resources (`resources/`)**

💡 Aquí está el cambio más importante:
👉 **Toda la lógica CRUD vive dentro de las clases Resource**

---

## 📌 `resources/categoria_resource.py`

```python
from flask_restful import Resource
from flask import request
from db import db
from models.categoria import CategoriasTable

class CategoriaListResource(Resource):

    def get(self):
        categorias = CategoriasTable.query.all()
        return [
            {'id': c.id, 'nombre': c.nombre}
            for c in categorias
        ]

    def post(self):
        data = request.get_json()

        nueva_categoria = CategoriasTable(
            nombre=data['nombre']
        )

        db.session.add(nueva_categoria)
        db.session.commit()

        return {
            'id': nueva_categoria.id,
            'nombre': nueva_categoria.nombre
        }, 201


class CategoriaResource(Resource):

    def get(self, id):
        categoria = CategoriasTable.query.get(id)

        if not categoria:
            return {'message': 'Categoría no encontrada'}, 404

        return {
            'id': categoria.id,
            'nombre': categoria.nombre
        }

    def put(self, id):
        data = request.get_json()
        categoria = CategoriasTable.query.get(id)

        if not categoria:
            return {'message': 'Categoría no encontrada'}, 404

        categoria.nombre = data['nombre']
        db.session.commit()

        return {
            'id': categoria.id,
            'nombre': categoria.nombre
        }

    def delete(self, id):
        categoria = CategoriasTable.query.get(id)

        if not categoria:
            return {'message': 'Categoría no encontrada'}, 404

        db.session.delete(categoria)
        db.session.commit()

        return {'message': 'Categoría eliminada'}
```

---

## 📌 `resources/post_resource.py`

```python
from flask_restful import Resource
from flask import request
from db import db
from models.post import PostTable

class PostListResource(Resource):

    def get(self):
        posts = PostTable.query.all()
        return [
            {
                'id': p.id,
                'titulo': p.titulo,
                'contenido': p.contenido,
                'fecha': str(p.fecha),
                'categoria_id': p.categoria_id
            }
            for p in posts
        ]

    def post(self):
        data = request.get_json()

        nuevo_post = PostTable(
            titulo=data['titulo'],
            contenido=data['contenido'],
            fecha=data['fecha'],
            categoria_id=data['categoria_id']
        )

        db.session.add(nuevo_post)
        db.session.commit()

        return {
            'id': nuevo_post.id,
            'titulo': nuevo_post.titulo
        }, 201


class PostResource(Resource):

    def get(self, id):
        post = PostTable.query.get(id)

        if not post:
            return {'message': 'Post no encontrado'}, 404

        return {
            'id': post.id,
            'titulo': post.titulo,
            'contenido': post.contenido,
            'fecha': str(post.fecha),
            'categoria_id': post.categoria_id
        }

    def put(self, id):
        data = request.get_json()
        post = PostTable.query.get(id)

        if not post:
            return {'message': 'Post no encontrado'}, 404

        post.titulo = data['titulo']
        post.contenido = data['contenido']
        post.fecha = data['fecha']
        post.categoria_id = data['categoria_id']

        db.session.commit()

        return {
            'id': post.id,
            'titulo': post.titulo
        }

    def delete(self, id):
        post = PostTable.query.get(id)

        if not post:
            return {'message': 'Post no encontrado'}, 404

        db.session.delete(post)
        db.session.commit()

        return {'message': 'Post eliminado'}
```

---

# 5️⃣ **Configurar `app.py`**

```python
from flask import Flask
from flask_restful import Api
from db import db
from flask_migrate import Migrate

from resources.categoria_resource import CategoriaListResource, CategoriaResource
from resources.post_resource import PostListResource, PostResource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/db_blogs_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Rutas RESTful
api.add_resource(CategoriaListResource, '/categorias')
api.add_resource(CategoriaResource, '/categorias/<int:id>')

api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/posts/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
```



---

# 🚀 **Resultado final**

✔ API REST limpia
✔ Código alineado con documentación oficial
✔ Arquitectura profesional
✔ Lista para escalar

