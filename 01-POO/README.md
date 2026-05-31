








# Carrera de Caballos 🏇

## Guia para estudiantes

---

## Parte 1: Repaso de POO

Antes de meter mano en el codigo, aseguremonos de que estos conceptos esten claros.

### Clase y Objeto

Una **clase** es como un molde. El **objeto** es lo que sale de ese molde.

```python
# Clase = molde
class Auto:
    pass

# Objeto = instancia concreta
mi_auto = Auto()
otro_auto = Auto()
```

`mi_auto` y `otro_auto` son dos objetos distintos, aunque los dos se crearon con el mismo molde `Auto`.

### Atributos

Son los datos que vive dentro del objeto. Se definen en `__init__` y se acceden con `self`:

```python
class Alumno:
    def __init__(self, nombre):
        self.nombre = nombre   # <-- atributo
        self.nota = 0          # <-- atributo
```

Cada objeto tiene SUS propios atributos. Si creo dos alumnos, cada uno tiene su nombre y su nota independientes.

### Metodos

Son funciones que pertenecen al objeto. Operan sobre los atributos del objeto:

```python
class Alumno:
    def __init__(self, nombre):
        self.nombre = nombre
        self.nota = 0

    def poner_nota(self, nota):        # <-- metodo
        self.nota = nota

    def aprobo(self):                  # <-- metodo
        return self.nota >= 6
```

### `self`

Es el "yo" del objeto. Cuando haces:

```python
a = Alumno("Ana")
b = Alumno("Luis")
```

Dentro de `__init__`, cuando se ejecuta con Ana, `self` **es** Ana. Cuando se ejecuta con Luis, `self` **es** Luis. `self` es lo que permite que cada objeto maneje sus propios datos.

### `__init__`

El **constructor**. Python lo llama automaticamente cuando escribis `Alumno("Ana")`. Su trabajo es inicializar los atributos del objeto nuevo.

### Composicion

Una clase puede tener objetos de otra clase como atributos:

```python
class Rueda:
    pass

class Auto:
    def __init__(self):
        self.ruedas = [Rueda() for _ in range(4)]  # composicion
```

Un `Auto` **tiene** 4 `Rueda`. Eso es composicion.

---

## Parte 2: El problema

Vamos a hacer un juego de carreras de caballos donde:

- Hay **4 caballos** compitiendo. Cada uno avanza una cantidad aleatoria por turno.
- El **jugador** (vos) arranca con 100 monedas y apuesta por un caballo.
- La carrera se corre en la consola y se ve el progreso en tiempo real.
- Si tu caballo gana, cobras el monto apostado multiplicado por el pago de ese caballo.
- Si perdes, perdes la plata apostada.
- Seguis jugando rondas hasta que te quieras ir o te quedes sin saldo.

### Los caballos

| Nombre     | Velocidad | Pago |
|------------|-----------|------|
| Rayo       | 2 a 5     | x1.5 |
| Trueno     | 1 a 5     | x2   |
| Relampago  | 1 a 4     | x3   |
| Tornado    | 1 a 3     | x5   |

Fijate el balance: a menor velocidad, mayor pago. Apostar a Tornado es mas riesgoso pero si gana, cobras 5 veces lo apostado.

---

## Parte 3: Que tenes que construir

### Clase `Caballo`

Representa un caballo de carrera.

**Atributos que necesita:**
- nombre
- velocidad_min
- velocidad_max
- pago (el multiplicador)
- posicion (arranca en 0)

**Metodos que necesita:**
- `avanzar()`: suma un valor aleatorio entre velocidad_min y velocidad_max a la posicion
- `reiniciar()`: vuelve la posicion a 0

**Pistas:**
- `random.randint(a, b)` te da un entero aleatorio entre a y b inclusive
- No te olvides de importar `import random` al principio del archivo
- `avanzar()` no recibe parametros ni devuelve nada, solo modifica `self.posicion`

### Clase `Jugador`

Representa al usuario del juego.

**Atributos que necesita:**
- nombre
- saldo (arranca en 100)

**Metodos que necesita:**
- `apostar(monto)`: descuenta el monto del saldo. Tiene que verificar que el monto sea valido (mayor a 0 y menor o igual al saldo). Devuelve `True` si se pudo, `False` si no.
- `cobrar(monto)`: suma las ganancias al saldo

**Pistas:**
- `apostar()` devuelve `True` o `False` para que el programa principal sepa si la apuesta fue exitosa
- `cobrar()` recibe el monto TOTAL a sumar (monto_apostado * pago), no la ganancia neta
- Usa `int(monto)` para convertir a entero por si el calculo da decimales

### Clase `Carrera`

Gestiona toda la carrera.

**Atributos que necesita:**
- caballos (lista de objetos `Caballo`)
- distancia_meta (cuanto hay que avanzar para ganar)
- ganador (arranca en `None`)

**Metodos que necesita:**
- `iniciar()`: ejecuta la carrera. Mientras no haya ganador, todos los caballos avanzan y se muestra el progreso. Cuando alguien llega a la meta, termina y devuelve el ganador.
- `reiniciar()`: pone todo en estado inicial para la proxima carrera

**Pistas:**
- `iniciar()` tiene un bucle que NO para hasta que hay ganador
- En cada vuelta del bucle: llama a `avanzar()` de cada caballo, despues verifica si alguno supero la distancia_meta
- Para verificar, recorrer la lista de caballos y ver si `caballo.posicion >= self.distancia_meta`
- Importante: una vez que se asigna `self.ganador`, el bucle tiene que terminar
- `reiniciar()` llama a `reiniciar()` de cada caballo y pone `self.ganador = None`

---

## Parte 4: El programa principal (`main`)

El `main()` es el que coordina todo. No pertenece a ninguna clase, es una funcion aparte.

**Flujo:**

1. Mostrar cartel de bienvenida
2. Pedir nombre del jugador y crear un `Jugador`
3. Crear los 4 `Caballo` y una `Carrera`
4. Entrar en un bucle infinito (`while True`) que:
   a. Muestra el saldo del jugador
   b. Muestra la tabla de caballos disponibles
   c. Pide al usuario que elija un caballo (1-4) o que escriba "salir"
   d. Pide el monto a apostar
   e. Verifica que la apuesta sea valida (llamando a `jugador.apostar()`)
   f. Ejecuta la carrera (`carrera.iniciar()`)
   g. Muestra el ganador
   h. Si el jugador gano: calcula ganancia y llama a `jugador.cobrar()`
   i. Si perdio: muestra mensaje de perdida
   j. Pregunta si quiere jugar otra ronda
   k. Si el saldo llega a 0 o el jugador no quiere seguir: `break`

**Pistas para la interfaz con Rich:**

- `console = Console()` crea la consola
- `console.print()` imite texto con formato
- `Panel.fit("texto", border_style="yellow")` crea un cartel con borde
- `Table(title="...", box=...)` crea tablas. Agregas columnas con `add_column()` y filas con `add_row()`
- `Prompt.ask("pregunta")` pide texto al usuario
- Ninguna de estas funciones es complicada - lee el codigo existente para ver ejemplos

---

## Parte 5: Pistas generales

### Sobre la animacion de la carrera

Para que se vea el progreso, adentro del bucle de `iniciar()`:

1. Limpia la pantalla con `console.clear()`
2. Hace que todos los caballos avancen
3. Verifica si hay ganador
4. Muestra una tabla con el estado actual
5. Espera un poco (`time.sleep(0.1)`)

Esto da la ilusion de movimiento. Proba con distintos valores de sleep para hacer la carrera mas rapida o mas lenta.

### Sobre las barras de progreso

Para dibujar una barra como `█████░░░░░░` tenes que:

1. Calcular la proporcion: `posicion / distancia_meta`
2. Usar `min(proporcion, 1.0)` para que nunca pase de 1
3. Multiplicar por el ancho que quieras (ej: 25) y convertir a entero
4. Crear el string con `"█" * lleno + "░" * (ancho - lleno)`

### Sobre la validacion de entrada

Siempre que pedis algo al usuario, puede pasar cualquier cosa. Usa `.isdigit()` para verificar que sea un numero antes de usar `int()`. Esto evita que el programa explote si el usuario escribe "tres" en vez de "3".

### Sobre el flujo de la apuesta

```python
if jugador.apostar(monto):   # intenta descontar
    # aca la apuesta fue exitosa
    # ejecutar carrera, ver resultado, etc.
else:
    # aca la apuesta fallo (saldo insuficiente o monto invalido)
    # mostrar error y volver
```

### Sobre las ganancias

Si apostaste 10 monedas a un caballo con pago x3 y gana:

```python
ganancia = 10 * 3   # = 30
jugador.cobrar(ganancia)   # se suman 30 al saldo
```

La ganancia **neta** (lo que realmente ganaste) es `ganancia - monto_apostado`.

---

## Parte 6: Checklist para saber si estas listo

- [ ] `Caballo` tiene todos sus atributos y metodos
- [ ] `Caballo.avanzar()` usa `random.randint()` correctamente
- [ ] `Jugador` tiene nombre, saldo, apostar() y cobrar()
- [ ] `Jugador.apostar()` devuelve `False` si no hay suficiente saldo
- [ ] `Carrera` recibe una lista de caballos
- [ ] `Carrera.iniciar()` tiene un bucle que avanza caballos y detecta ganador
- [ ] `Carrera.iniciar()` limpia pantalla y muestra progreso en cada paso
- [ ] El `main()` tiene el bucle de rondas con entrada de usuario
- [ ] Validaste que el usuario ingrese numeros validos
- [ ] Probaste el juego al menos una vez completa
- [ ] Probaste que pasa si el saldo llega a 0

---

## Bonus: Si te sobra tiempo

1. Agrega mas caballos (inventa nombre, velocidad y pago)
2. Muestra el historial de las ultimas 3 carreras (quien gano y por cuanto)
3. Permitile al jugador apostar a 2 caballos distintos en la misma carrera
4. Hace que la distancia de la meta sea aleatoria (entre 80 y 120)
