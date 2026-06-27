import psycopg2

# Credenciales de nuestra bd

# Credenciales 
# postgresql://neondb_owner:npg_BGEC5YV8oIbS@ep-withered-rain-acxpdk1t-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
# MOTOR_BD://USER:CONTRASEÑA@HOST/NOMBRE_BD
DATABASE_CONFIG = {
    'dbname': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_BGEC5YV8oIbS',
    'host': 'ep-withered-rain-acxpdk1t-pooler.sa-east-1.aws.neon.tech',
}

# Vamos a crear una funcion para conectarnos
def get_db_conection():
   conn = psycopg2.connect(**DATABASE_CONFIG)
   return conn

# Voy a crear una funciona para cada vez que se levante el servidor
# esta se ejecute automaticamente
# Es para crear las tablas si estas no estan creadas
def create_tables():
   # Todavia aun no tenemos ninguna conexion
   conn = None
   try:
      conn = get_db_conection() #La conexion
      with conn: # Con esta conexion
         # Vamos a ejecutar codigo SQL
         with conn.cursor() as cursor: # Esta accion me perimita ejecutar SQL
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
               
               print("Tablas creadas exitosamente")
   except Exception as e:
      print(e)
   finally:
      if conn:
         conn.close()