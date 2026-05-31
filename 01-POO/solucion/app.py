"""
CARRERA DE CABALLOS CON APUESTAS - POO
"""

import random
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

console = Console()


class Caballo:
    def __init__(self, nombre, velocidad_min, velocidad_max, pago):
        self.nombre = nombre
        self.velocidad_min = velocidad_min
        self.velocidad_max = velocidad_max
        self.pago = pago
        self.posicion = 0

    def avanzar(self):
        avance = random.randint(self.velocidad_min, self.velocidad_max)
        self.posicion += avance

    def reiniciar(self):
        self.posicion = 0


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.saldo = 100

    def apostar(self, monto):
        if monto <= 0 or monto > self.saldo:
            return False
        self.saldo -= monto
        return True

    def cobrar(self, monto):
        self.saldo += int(monto)


class Carrera:
    def __init__(self, caballos, distancia_meta=100):
        self.caballos = caballos
        self.distancia_meta = distancia_meta
        self.ganador = None

    def _barra(self, posicion, ancho=25):
        proporcion = min(posicion / self.distancia_meta, 1.0)
        lleno = int(proporcion * ancho)
        return "█" * lleno + "░" * (ancho - lleno)

    def _tabla_carrera(self):
        table = Table(title="CARRERA EN CURSO", title_style="bold yellow",
                      header_style="bold cyan", box=box.ROUNDED)
        table.add_column("Caballo", style="bold", width=14)
        table.add_column("Progreso", width=30)
        table.add_column("Pos", justify="right", width=5)

        for c in self.caballos:
            barra = self._barra(c.posicion)
            estilo = "green" if c is self.ganador else "white"
            table.add_row(f"[{estilo}]{c.nombre}[/]", barra,
                          f"[{estilo}]{c.posicion}[/]")
        return table

    def iniciar(self):
        while self.ganador is None:
            console.clear()
            for c in self.caballos:
                c.avanzar()
                if c.posicion >= self.distancia_meta and self.ganador is None:
                    self.ganador = c
            console.print(self._tabla_carrera())
            time.sleep(0.1)
        return self.ganador

    def reiniciar(self):
        self.ganador = None
        for c in self.caballos:
            c.reiniciar()


def tabla_caballos(caballos):
    table = Table(title="CABALLOS DISPONIBLES", title_style="bold cyan",
                  header_style="bold magenta", box=box.ROUNDED)
    table.add_column("#", justify="right", style="dim", width=3)
    table.add_column("Nombre", style="bold", width=14)
    table.add_column("Velocidad", justify="center", width=12)
    table.add_column("Pago", justify="center", width=8)
    for i, c in enumerate(caballos, 1):
        table.add_row(str(i), c.nombre, f"{c.velocidad_min}-{c.velocidad_max}",
                      f"x{c.pago}")
    return table


def main():
    console.clear()
    console.print(Panel.fit("[bold yellow]CARRERA DE CABALLOS[/]\n\n"
                  "[white]Aposta por tu caballo favorito y gana premios[/]",
                  border_style="yellow"))

    nombre = Prompt.ask("[bold cyan]Tu nombre[/]")
    jugador = Jugador(nombre)

    caballos = [
        Caballo("Rayo", 2, 4, 1.5),
        Caballo("Trueno", 1, 5, 2.0),
        Caballo("Relampago", 1, 4, 3.0),
        Caballo("Tornado", 1, 3, 5.0),
    ]

    carrera = Carrera(caballos, 100)

    while True:
        console.clear()

        color = "green" if jugador.saldo > 20 else "red"
        console.print(Panel(f"Saldo: {jugador.saldo} monedas",
                            border_style=color))

        if jugador.saldo <= 0:
            console.print("[bold red]Te quedaste sin saldo! Fin.[/]")
            break

        console.print(tabla_caballos(caballos))

        opcion = Prompt.ask("[yellow]Escoje caballo (1-4) o 'salir'[/]", default="1")
        if opcion.lower() in ("salir", "s", "exit"):
            console.print(f"[green]Gracias por jugar! Saldo final: {jugador.saldo}[/]")
            break

        if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 4:
            console.print("[red]Opcion invalida[/]")
            Prompt.ask("[dim]Enter para continuar...[/]")
            continue

        caballo_elegido = caballos[int(opcion) - 1]

        monto_str = Prompt.ask(f"[yellow]Cuanto apuestas a {caballo_elegido.nombre}?[/]",
                               default="10")
        if not monto_str.isdigit():
            console.print("[red]Monto invalido[/]")
            Prompt.ask("[dim]Enter para continuar...[/]")
            continue

        monto = int(monto_str)
        if not jugador.apostar(monto):
            console.print("[red]Saldo insuficiente[/]")
            Prompt.ask("[dim]Enter para continuar...[/]")
            continue

        console.print(f"\n[bold]{jugador.nombre} apuesta {monto} a "
                      f"[yellow]{caballo_elegido.nombre}[/]![/]")
        time.sleep(1)

        ganador = carrera.iniciar()

        console.print(Panel.fit(f"[green]GANADOR: {ganador.nombre}[/]",
                                border_style="green"))

        if ganador is caballo_elegido:
            ganancia = int(monto * caballo_elegido.pago)
            jugador.cobrar(ganancia)
            console.print(f"[green]GANASTE! Recibes {ganancia} monedas "
                          f"(ganancia neta: {ganancia - monto})[/]")
        else:
            console.print(f"[red]Perdiste {monto} monedas. Gano {ganador.nombre}.[/]")

        console.print(Panel(f"Saldo actual: {jugador.saldo} monedas",
                            border_style="green" if jugador.saldo > 20 else "red"))

        carrera.reiniciar()

        seguir = Prompt.ask("[yellow]Otra ronda?[/] (s/n)", default="s")
        if seguir.lower() not in ("s", "si", "y", "yes"):
            console.print(f"[green]Gracias por jugar! Saldo final: {jugador.saldo}[/]")
            break


if __name__ == "__main__":
    main()
