from src.agent import agent

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from pyfiglet import figlet_format

banner = figlet_format("OSINT SCANNER", font="slant")

console=Console()

def mostrar_menu():
    op = 0
    while op != 1 and op != 2:
        console.print(banner, style="cyan")
        titulo = Text("OSINT RECON AGENT", style="bold cyan", justify="center")
        opciones = Text()
        # opciones.append(banner, style="cyan")
        opciones.append("\n[1] ", style="bold green")
        opciones.append("Analizar dominio\n")
        opciones.append("[2] ", style="bold red")
        opciones.append("Salir\n")
        console.print(Panel(opciones, title=titulo, border_style="cyan"))
        op = int(input("\nSelecciona una opción: "))
    return op

while True:
    op = mostrar_menu()

    if op==1:
        dominio=input("Introduce el dominio que quieres analizar:")
        inputs={"messages": [{"role":"user", "content":f"Analiza el dominio: {dominio}"}]}

        with console.status("[cyan]Analizando dominio...", spinner="dots"):
            for chunk in agent.stream(inputs, stream_mode="updates"):
                if "model" in chunk:
                    mensaje = chunk["model"]["messages"][-1]

                    if isinstance(mensaje.content, str):
                        md = Markdown(mensaje.content)
                        console.print(md)
    elif op==2:
        print("Hasta pronto compi!")
        exit()
    else:
        print("Formato de respuesta incorrecto.")