# Flask + PostgreSQL — Productos y Categorías

Construí conmigo.

Hasta ahora siempre trabajaron con datos en memoria. Listas, diccionarios, todo se borraba cuando apagaban el servidor. Hoy damos el salto a una base de datos real.

---

## El problema

Necesitamos un sistema para administrar productos de un catálogo. Cada producto tiene nombre, precio, stock y pertenece a una categoría. Los datos TIENEN que sobrevivir a un reinicio del servidor.

Vamos a construir:

```
GET    /categorias       → listar todas
POST   /categorias       → crear una
GET    /categorias/<id>  → traer una
PUT    /categorias/<id>  → actualizar
DELETE /categorias/<id>  → eliminar (solo si está vacía)

GET    /productos          → listar todos (con su categoría)
POST   /productos          → crear uno
GET    /productos/<id>     → traer uno
PUT    /productos/<id>     → actualizar
DELETE /productos/<id>     → eliminar
```

**Las categorías las hacemos juntos.** Los productos los hacen ustedes.

---

## 1. Setup

### Entorno virtual

Aísla las dependencias del proyecto:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

La terminal muestra `(venv)` al inicio.

### Instalar dependencias

```bash
pip install flask psycopg2-binary
```

### Crear la base de datos

Con PostgreSQL corriendo, abrí **pgAdmin** (o terminal con `psql -U postgres`) y ejecutá:

```sql
CREATE DATABASE tienda;
```

No crees tablas todavía. Eso lo hace Flask cuando arranque.

### Estructura del proyecto

```
Flask-PostgreSQL/
├── GUIA.md
├── db.py              ← conexión a la BD
├── category_resource.py  ← CRUD de categorías
├── product_resource.py   ← VAS A CREAR VOS
└── app.py             ← rutas
```

---

## 2. El esquema de la BD

Vamos a trabajar con dos tablas relacionadas:

**categorias**

| Columna | Tipo | ¿Qué guarda? |
|---------|------|-------------|
| id | SERIAL | Número único, se genera solo |
| nombre | VARCHAR(100) | Ej: "Electrónica", "Ropa" |
| descripcion | TEXT | Opcional |
| created_at | TIMESTAMP | Fecha de creación, se genera solo |

**productos**

| Columna | Tipo | ¿Qué guarda? |
|---------|------|-------------|
| id | SERIAL | Número único |
| nombre | VARCHAR(255) | Obligatorio |
| descripcion | TEXT | Opcional |
| precio | NUMERIC(10,2) | Con decimales |
| stock | INTEGER | Cantidad disponible |
| categoria_id | INTEGER | ¿A qué categoría pertenece? |

**Regla importante:** un producto siempre pertenece a UNA categoría. Si intentás borrar una categoría que tiene productos, PostgreSQL lo rechaza.

> **Pregunta:** ¿Por qué creen que existe `categoria_id` dentro de `productos` en vez de al revés?

---

## 3. Paso 1 — Conexión a la BD (`db.py`)

Primera decisión: ¿cómo habla Flask con PostgreSQL?

Necesitamos una función que nos dé una conexión cada vez que la necesitemos, y otra que cree las tablas cuando el servidor arranque.

Creá `db.py`:

```python
import psycopg2

DATABASE_CONFIG = {
    'dbname': 'tienda',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': 5432
}
```

> Si tu PostgreSQL tiene otro usuario o contraseña, cambiá esos valores.

### get_db_connection()

Escribí una función que devuelva una conexión nueva:

```python
def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn
```

`**DATABASE_CONFIG` es como decirle a psycopg2 "tomá este diccionario como si fueran parámetros separados".

### create_tables()

Necesitamos crear las tablas cuando arranca la app. La función tiene que:

1. Conectarse a la BD
2. Crear `categorias` (si no existe)
3. Crear `productos` (si no existe, con FK a categorias)
4. Insertar 5 categorías de ejemplo
5. Cerrar la conexión

**Pista 1 — `IF NOT EXISTS`:** `CREATE TABLE IF NOT EXISTS` evita errores si la tabla ya existe y el servidor se reinicia.

**Pista 2 — FK (Foreign Key):** para decir que `categoria_id` apunta a `categorias(id)`:

```sql
categoria_id INTEGER NOT NULL REFERENCES categorias(id) ON DELETE RESTRICT
```

`ON DELETE RESTRICT` significa "no dejes borrar una categoría si tiene productos".

**Pista 3 — `ON CONFLICT`:** para insertar datos de ejemplo sin duplicar si el servidor se reinicia:

```sql
INSERT INTO categorias (nombre, descripcion) VALUES
    ('Electrónica', 'Dispositivos electrónicos y accesorios'),
    ('Ropa', 'Prendas de vestir para toda la temporada'),
    ('Hogar', 'Artículos para el hogar y decoración'),
    ('Deportes', 'Equipamiento e indumentaria deportiva'),
    ('Libros', 'Libros físicos y digitales')
ON CONFLICT (nombre) DO NOTHING
```

**Tu turno:** escribí `create_tables()` completo. Usá el patrón `try / finally` para asegurarte de cerrar la conexión incluso si hay error.

<details>
<summary>¿Cómo va quedando?</summary>

```python
def create_tables():
    conn = None
    try:
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('''CREATE TABLE IF NOT EXISTS categorias (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL UNIQUE,
                    descripcion TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    descripcion TEXT,
                    precio NUMERIC(10, 2) NOT NULL,
                    stock INTEGER NOT NULL DEFAULT 0,
                    categoria_id INTEGER NOT NULL REFERENCES categorias(id) ON DELETE RESTRICT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
                cursor.execute('''
                    INSERT INTO categorias (nombre, descripcion) VALUES
                        ('Electrónica', 'Dispositivos electrónicos y accesorios'),
                        ('Ropa', 'Prendas de vestir para toda la temporada'),
                        ('Hogar', 'Artículos para el hogar y decoración'),
                        ('Deportes', 'Equipamiento e indumentaria deportiva'),
                        ('Libros', 'Libros físicos y digitales')
                    ON CONFLICT (nombre) DO NOTHING
                ''')
        print('Tables created successfully')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if conn:
            conn.close()
```
</details>

---

## 4. Paso 2 — CRUD de categorías (`category_resource.py`)

Acá empieza la magia. Vamos a construir los 5 métodos del CRUD.

Cada método sigue el mismo patrón:

```
1. Abrir conexión
2. try:
3.     Ejecutar SQL
4.     Devolver resultado (jsonify + código HTTP)
5. except: devolver error
6. finally: cerrar conexión
```

### 4.1 — MÉTODO list()

Tiene que devolver TODAS las categorías como JSON.

```python
from db import get_db_connection
from flask import jsonify

class CategoryResource:
    def list(self):
        conn = get_db_connection()
        try:
            categorias = []
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT * FROM categorias ORDER BY id')
                    rows = cursor.fetchall()
                    for row in rows:
                        categorias.append({
                            'id': row[0],
                            'nombre': row[1],
                            'descripcion': row[2],
                            'created_at': str(row[3])
                        })
            return jsonify(categorias), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400
        finally:
            conn.close()
```

> **Notá:** `fetchall()` devuelve una lista de tuplas. Accedemos por índice: `row[0]` es el id, `row[1]` el nombre, etc.
>
> `created_at` lo convertimos a string porque `datetime` no es serializable a JSON.

### 4.2 — MÉTODO create(data)

El cliente nos manda un JSON con `nombre` y `descripcion`. Nosotros:

1. Validamos que `nombre` no esté vacío
2. Insertamos en la BD
3. Devolvemos el ID generado con código **201** (Created)

**Pista:** usá `RETURNING id` al final del INSERT para obtener el ID:

```python
cursor.execute(
    'INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s) RETURNING id',
    (nombre, descripcion)
)
new_id = cursor.fetchone()[0]
```

**Tu turno:** escribí `create(self, data)`.

<details>
<summary>Solución</summary>

```python
def create(self, data):
    conn = get_db_connection()
    try:
        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')

        if not nombre:
            return jsonify({'message': 'El nombre es obligatorio'}), 400

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s) RETURNING id',
                    (nombre, descripcion)
                )
                new_id = cursor.fetchone()[0]
        return jsonify({'message': 'Categoría creada', 'id': new_id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    finally:
        conn.close()
```
</details>

### 4.3 — MÉTODO get_by_id(categoria_id)

Buscar UNA categoría por su ID.

- Si existe → devolverla como JSON, código **200**
- Si no existe → `{'message': 'Categoría no encontrada'}`, código **404**

**Pista:** usá `fetchone()` en vez de `fetchall()`. Si es `None`, no existe.

**Tu turno:** escribí `get_by_id(self, categoria_id)`.

### 4.4 — MÉTODO update(categoria_id, data)

Actualizar nombre y/o descripción de una categoría.

Pasos:
1. Verificar que existe (si no → 404)
2. Tomar los valores nuevos (o mantener los viejos si no vienen)
3. Hacer el UPDATE

**Pista importante:** el cliente puede mandar SOLO el nombre, SOLO la descripción, o ambos. Usá `data.get('nombre', row[1])` — si no viene el campo, se conserva el valor actual que ya está en la BD.

**Tu turno:** escribí `update(self, categoria_id, data)`.

### 4.5 — MÉTODO delete(categoria_id)

Eliminar una categoría.

- Si no existe → 404
- Si existe → DELETE y devolver mensaje

> **¿Qué pasa si la categoría tiene productos?** `ON DELETE RESTRICT` hace que PostgreSQL rechace el DELETE. La excepción se captura en el `except` y se devuelve como error 400.

**Tu turno:** escribí `delete(self, categoria_id)`.

<details>
<summary>Solución completa de CategoryResource</summary>
Acá está el archivo completo por si te trabás:

```python
from db import get_db_connection
from flask import jsonify

class CategoryResource:
    def list(self):
        conn = get_db_connection()
        try:
            categorias = []
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT * FROM categorias ORDER BY id')
                    rows = cursor.fetchall()
                    for row in rows:
                        categorias.append({
                            'id': row[0],
                            'nombre': row[1],
                            'descripcion': row[2],
                            'created_at': str(row[3])
                        })
            return jsonify(categorias), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400
        finally:
            conn.close()

    def create(self, data):
        conn = get_db_connection()
        try:
            nombre = data.get('nombre')
            descripcion = data.get('descripcion', '')
            if not nombre:
                return jsonify({'message': 'El nombre es obligatorio'}), 400
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s) RETURNING id',
                        (nombre, descripcion)
                    )
                    new_id = cursor.fetchone()[0]
            return jsonify({'message': 'Categoría creada', 'id': new_id}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 400
        finally:
            conn.close()

    def get_by_id(self, categoria_id):
        conn = get_db_connection()
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT * FROM categorias WHERE id = %s', (categoria_id,))
                    row = cursor.fetchone()
                    if row is None:
                        return jsonify({'message': 'Categoría no encontrada'}), 404
                    return jsonify({
                        'id': row[0], 'nombre': row[1],
                        'descripcion': row[2], 'created_at': str(row[3])
                    }), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400
        finally:
            conn.close()

    def update(self, categoria_id, data):
        conn = get_db_connection()
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT * FROM categorias WHERE id = %s', (categoria_id,))
                    row = cursor.fetchone()
                    if row is None:
                        return jsonify({'message': 'Categoría no encontrada'}), 404
                    nombre = data.get('nombre', row[1])
                    descripcion = data.get('descripcion', row[2])
                    cursor.execute(
                        'UPDATE categorias SET nombre = %s, descripcion = %s WHERE id = %s',
                        (nombre, descripcion, categoria_id)
                    )
            return jsonify({'message': 'Categoría actualizada'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400
        finally:
            conn.close()

    def delete(self, categoria_id):
        conn = get_db_connection()
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT * FROM categorias WHERE id = %s', (categoria_id,))
                    row = cursor.fetchone()
                    if row is None:
                        return jsonify({'message': 'Categoría no encontrada'}), 404
                    cursor.execute('DELETE FROM categorias WHERE id = %s', (categoria_id,))
            return jsonify({'message': 'Categoría eliminada'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 400
        finally:
            conn.close()
```
</details>

---

## 5. Paso 3 — `app.py` (rutas de categorías)

Creá `app.py`:

```python
from flask import Flask, request
from db import create_tables
from category_resource import CategoryResource

app = Flask(__name__)
create_tables()


@app.route('/')
def home():
    return 'Hello Flask con PostgreSQL 🐘'
```

> **Notá:** `create_tables()` se llama UNA VEZ al arrancar. Si las tablas ya existen, `IF NOT EXISTS` las deja igual.

### Rutas de categorías

Agregá estos endpoints a `app.py`:

```python
@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    resource = CategoryResource()
    if request.method == 'GET':
        return resource.list()
    elif request.method == 'POST':
        data = request.get_json()
        return resource.create(data)


@app.route('/categorias/<int:categoria_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_categoria(categoria_id):
    resource = CategoryResource()
    if request.method == 'GET':
        return resource.get_by_id(categoria_id)
    elif request.method == 'PUT':
        data = request.get_json()
        return resource.update(categoria_id, data)
    elif request.method == 'DELETE':
        return resource.delete(categoria_id)
```

### ¡A probar!

```bash
python app.py
```

Probá estos endpoints con el navegador o Postman:

| Método | Ruta | ¿Qué tiene que pasar? |
|--------|------|----------------------|
| GET | /categorias | Devuelve las 5 categorías de ejemplo |
| POST | /categorias | Creá una nueva con `{"nombre": "Juguetes", "descripcion": "Para niños"}` |
| GET | /categorias/1 | Devuelve "Electrónica" |
| PUT | /categorias/1 | Cambiale el nombre con `{"nombre": "Electro"}` |
| DELETE | /categorias/3 | Borra "Hogar" (no tiene productos, debería funcionar) |
| DELETE | /categorias/1 | Intenta borrar "Electrónica" — **tiene que fallar** porque hay productos que la referencian |

> **¿Por qué falla el último?** `ON DELETE RESTRICT`. PostgreSQL no deja borrar una categoría si hay productos que apuntan a ella.

---

## 6. Reto — CRUD de Productos (`product_resource.py`)

Ahora solos. Tienen que crear `product_resource.py` con los mismos 5 métodos, pero para la tabla `productos`.

### R1 — GET /productos

Listar todos los productos. Pero atención: cuando el cliente ve la lista, necesita ver el **nombre de la categoría**, no solo el ID.

**Pista:** tenés que hacer un JOIN:

```sql
SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock,
       p.categoria_id, c.nombre AS categoria_nombre, p.created_at
FROM productos p
JOIN categorias c ON p.categoria_id = c.id
ORDER BY p.id
```

La respuesta debería verse así:

```json
{
  "id": 1,
  "nombre": "Auriculares Bluetooth",
  "descripcion": "Inalámbricos, cancelación de ruido",
  "precio": 89.99,
  "stock": 25,
  "categoria_id": 1,
  "categoria_nombre": "Electrónica",
  "created_at": "2026-06-14 11:00:00"
}
```

**Ojo:** `NUMERIC` en psycopg2 viene como `Decimal`, no como `float`. JSON no sabe serializar `Decimal`. Convertilo:

```python
'precio': float(row[3])
```

---

### R2 — POST /productos

Validaciones obligatorias:
- `nombre` no puede estar vacío
- `precio` es obligatorio
- `categoria_id` TIENE que existir en la tabla categorias

**Pista:** primero verificá que la categoría existe con un SELECT, y si no, devolvé 404 con mensaje "La categoría no existe".

```python
cursor.execute('SELECT id FROM categorias WHERE id = %s', (categoria_id,))
if cursor.fetchone() is None:
    return jsonify({'message': 'La categoría no existe'}), 404
```

---

### R3 — GET /productos/<id>

Traer UN producto con JOIN. Si no existe, 404.

**Pista:** es casi idéntico a `get_by_id` de categorías, pero con JOIN.

---

### R4 — PUT /productos/<id>

Actualizar un producto. Reglas:
- Si no existe → 404
- Si cambian de categoría → validar que la nueva exista
- Si no mandan un campo → conservar el valor actual

---

### R5 — DELETE /productos/<id>

Eliminar un producto. Si no existe → 404.

---

### Agregar las rutas a `app.py`

Cuando termines `product_resource.py`, agregá estos endpoints a `app.py`:

```python
from product_resource import ProductResource


@app.route('/productos', methods=['GET', 'POST'])
def productos():
    resource = ProductResource()
    if request.method == 'GET':
        return resource.list()
    elif request.method == 'POST':
        data = request.get_json()
        return resource.create(data)


@app.route('/productos/<int:producto_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_producto(producto_id):
    resource = ProductResource()
    if request.method == 'GET':
        return resource.get_by_id(producto_id)
    elif request.method == 'PUT':
        data = request.get_json()
        return resource.update(producto_id, data)
    elif request.method == 'DELETE':
        return resource.delete(producto_id)
```

---

## 7. Tips

```python
# Decimal → float (para JSON)
'precio': float(row[3])

# Verificar si un valor es None
if precio is None:
    return jsonify({'message': 'El precio es obligatorio'}), 400

# Validar FK
cursor.execute('SELECT id FROM categorias WHERE id = %s', (id,))
if cursor.fetchone() is None:
    return jsonify({'message': 'No existe'}), 404

# RETURNING id
cursor.execute('INSERT INTO ... RETURNING id', datos)
nuevo_id = cursor.fetchone()[0]

# UPDATE parcial
nombre = data.get('nombre', row_actual[1])
```

---

## 8. Checklist

- [ ] Creé el entorno virtual
- [ ] Instalé `flask` y `psycopg2-binary`
- [ ] Creé la base de datos `tienda` en PostgreSQL
- [ ] Escribí `db.py` con `get_db_connection()` y `create_tables()`
- [ ] Escribí los 5 métodos de `CategoryResource`
- [ ] Probé GET /categorias → funciona
- [ ] Probé POST /categorias → funciona
- [ ] Probé DELETE /categorias/1 → falla (tiene productos)
- [ ] R1 — GET /productos devuelve lista con JOIN
- [ ] R2 — POST /productos crea y valida datos
- [ ] R3 — GET /productos/<id> devuelve uno o 404
- [ ] R4 — PUT /productos/<id> actualiza o 404
- [ ] R5 — DELETE /productos/<id> elimina o 404
