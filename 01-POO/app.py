import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table


class Caballo:
   # Para crear los atributos de una clas, utilizamos
   # el metodo init
   def __init__(self, 
                nombre, 
                velocidad_min, 
                velocidad_max, 
                pago, 
                ):
      self.nombre = nombre
      self.velocidad_min = velocidad_min
      self.velocidad_max = velocidad_max
      self.pago = pago
      self.posicion = 0

   def avanzar(self):
      #  0  +  3
      #  posicion = 3
      # Aqui genera un numero al azar entre la velo min y max
      avanze = random.randint(self.velocidad_min, self.velocidad_max)
      self.posicion = self.posicion + avanze

   def reiniciar(self):
      self.posicion = 0

class Jugador:
   def __init__(self, nombre):
      self.nombre = nombre
      self.saldo = 100

   def apostar(self, monto):
      if monto <= 0 or monto > self.saldo:
         return False

      self.saldo = self.saldo - monto
      return True
   
   def cobrar(self, monto):
      self.saldo = self.saldo + int(monto)

class Carrera:
   def __init__(self, caballos, distancia_meta=100):
      self.caballos = caballos
      self.distancia_meta = distancia_meta
      self.ganador = None

   # funcion con _ hace referencia aun metodo privado
   # o un metodo interno de la clase
   def _barra(self, posicion, ancho=25):
      proporcion = posicion / self.distancia_meta
      # 85 / 100 = 0.85
      lleno = int(proporcion * ancho)
      return "█" * lleno + " " * (ancho - int(lleno))
   
   def _tabla_carrera(self):
      table = Table(title="CARRERA EN CURSO")

      table.add_column("Caballo")
      table.add_column("Pogreso", width=30)
      table.add_column("Pos")

      for caballo in self.caballos:
         # Aqui vamos actualizar la barra de progreso x caballo
         barra = self._barra(caballo.posicion)
         table.add_row(caballo.nombre, barra, str(caballo.posicion))
      
      return table
   
   def iniciar(self):
      # Bucle de 2 tipos => Finitos e Infinitos
      # Finito => for este tiene un numero definido de iteraciones (repetacion)
      # Infinito => while este se repeti hasta que cumpla con una condicion
      while self.ganador is None:
         # Este bucle se dentra cuando exista un ganador
         console.clear()
         for caballo in self.caballos:
            caballo.avanzar()
            # Tengo que controlar si un caballo ya paso o llego a la meta
            if caballo.posicion >= self.distancia_meta:
               self.ganador = caballo
               break
            
         console.print(self._tabla_carrera())
         time.sleep(0.1)

      return self.ganador
         
   def reiniciar(self):
      self.ganador = None
      for caballo in self.caballos:
         caballo.reiniciar()


# Aqui vendra toda la logica de nuestro juego
# Siempre limpien primero la consola
console = Console()
console.clear()

console.print(Panel.fit("[yellow]CARRERA DE CABALLOS", border_style="blue"))
nombre = Prompt.ask("[green]Tu nombre:")
jugador = Jugador(nombre)

# Crear los caballos
caballos = [
   Caballo("Rayo", 2, 5, 1.5),
   Caballo("Trueno", 1, 5, 2),
   Caballo("Relampago", 1, 4, 3),
   Caballo("Tornado", 1, 3, 5)
]

carrera = Carrera(caballos)

# ¿Porque while True?
# Porque queremos que el juego se repita hasta que el jugador decida salir

while True:
   console.clear()

   console.print(Panel.fit(f"Saldo {jugador.saldo}"))

   table = Table(title="CABALLOS DISPONIBLES")
   table.add_column("#")
   table.add_column("Nombre")
   table.add_column("Velocidad")
   table.add_column("Pago")

   for index, caballo in enumerate(caballos):
      table.add_row(str(index + 1), caballo.nombre, f"{caballo.velocidad_min}-{caballo.velocidad_max}", str(caballo.pago))

   console.print(table)
   
   opcion = Prompt.ask("Escoge un caballo (1-4)")

   # Si yo coloco la opcion 1 
   # Restamos  - 1 , para poder apuntar al indice correcto
   caballo_elegido = caballos[int(opcion) - 1]

   monto = Prompt.ask("Monto a apostar", default="10")

   jugador.apostar(int(monto)) # Aqui apuesto el jugador

   ganador = carrera.iniciar()

   console.print(Panel.fit(f"El ganador es {ganador.nombre}"))

   if ganador is caballo_elegido:
      ganacia =  int(monto)  * caballo_elegido.pago
      jugador.cobrar(ganacia)

      console.print(Panel.fit(f"Felicidades ganaste {ganacia}"))
   else:
      console.print(Panel.fit(f"Lo siento, perdiste tu apuesta de {monto}"))

   carrera.reiniciar()