from src.agent import agent
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich.spinner import Spinner
from pyfiglet import figlet_format
from reports.pdf_generator import generar_pdf
import questionary
import json
from questionary import Style
from src.structured_agent import analizar_dominio_estructurado
from src.scorer import calcular_score

console = Console()

estilo_menu = Style([
    ('qmark', 'fg:cyan bold'),
    ('question', 'fg:white bold'),
    ('answer', 'fg:cyan bold'),
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan bold'),
    ('selected', 'fg:green bold'),
    ('separator', 'fg:cyan'),
    ('instruction', 'fg:white'),
])

def mostrar_banner():
    banner = figlet_format("OSINT AI CLI", font="doom")
    titulo = Text(banner, style="bold green")
    subtitulo = Text()
    subtitulo.append("[ ", style="green")
    subtitulo.append("Reconocimiento OSINT con Inteligencia Artificial", style="bold white")
    subtitulo.append(" ]", style="green")
    autor = Text()
    autor.append("[ ", style="green")
    autor.append("Desarrollado por ", style="dim white")
    autor.append("Alba Mora", style="bold green")
    autor.append(" · Proyecto Final IA Automatización 2026", style="dim white")
    autor.append(" ]", style="green")
    disclaimer = Text(justify="center")
    disclaimer.append("⚠  ", style="bold yellow")
    disclaimer.append("SOLO PARA USO ACADÉMICO Y EDUCATIVO", style="bold yellow")
    disclaimer.append("  ⚠", style="bold yellow")
    disclaimer.append("\n   Esta herramienta está diseñada únicamente con fines de aprendizaje.", style="dim yellow")
    disclaimer.append("\n   El uso no autorizado contra sistemas ajenos es ilegal.", style="dim yellow")
    console.print(titulo, justify="center")
    console.print(subtitulo, justify="center")
    console.print(autor, justify="center")
    console.print()
    console.print(Panel(disclaimer, border_style="yellow", padding=(0, 2)), justify="center")
    console.print()

def mostrar_menu():
    return questionary.select(
        "¿Qué quieres hacer?",
        choices=[
            questionary.Choice("⚡ Análisis completo", value=1),
            questionary.Choice("🔧 Análisis personalizado", value=2),
            questionary.Choice("🔍 Escanear secretos en GitHub", value=3),
            questionary.Choice("❌  Salir", value=4),
        ],
        style=estilo_menu
    ).ask()

def mostrar_submenu():
    return questionary.checkbox(
        "Selecciona las herramientas:",
        choices=[
            questionary.Choice("🌐 Subdominios (crt.sh)", value="Subdominios (crt.sh)"),
            questionary.Choice("📋 WHOIS", value="WHOIS"),
            questionary.Choice("🔗 Registros DNS", value="Registros DNS"),
            questionary.Choice("🔒 Headers HTTP", value="Headers HTTP"),
            questionary.Choice("⚠️  Filtraciones (LeakCheck)", value="Filtraciones (LeakCheck)"),
        ],
        style=estilo_menu
    ).ask()

def construir_prompt(dominio, herramientas):
    if herramientas is None:
        return f"Realiza un análisis OSINT completo del dominio {dominio} usando todas las herramientas disponibles."
    nombres = {
        "Subdominios (crt.sh)": "get_subdomains",
        "WHOIS": "get_whois_info",
        "Registros DNS": "get_dns_records",
        "Headers HTTP": "get_http_headers",
        "Filtraciones (LeakCheck)": "check_hibp"
    }
    tools_seleccionadas = [nombres[h] for h in herramientas]
    tools_str = ", ".join(tools_seleccionadas)
    return f"Analiza el dominio {dominio} usando ÚNICAMENTE estas herramientas: {tools_str}. No uses ninguna otra."

while True:
    mostrar_banner()
    op = mostrar_menu()

    # SALIR
    if op == 4:
        console.print("\n[bold green]¡Hasta pronto!. 🤖⚡[/bold green]\n")
        break

    # ESCANEAR SECRETOS EN GITHUB
    elif op == 3:
        objetivo = questionary.text(
            "Introduce usuario u organización de GitHub:",
            style=estilo_menu
        ).ask()

        if objetivo:
            from src.secrets_scanner import escanear_secretos_github
            with console.status("[cyan]Escaneando repositorios...", spinner="dots"):
                resultado_scan = escanear_secretos_github.invoke({"objetivo": objetivo})
            console.print(Markdown(resultado_scan))
        else:
            console.print("[red]Usuario no válido.[/red]")
        continue

    # ANÁLISIS DE DOMINIO (completo o personalizado)
    dominio = questionary.text(
        "Introduce el dominio a analizar:",
        style=estilo_menu
    ).ask()

    if not dominio:
        console.print("[red]Dominio no válido.[/red]")
        continue

    herramientas = None
    if op == 2:
        herramientas = mostrar_submenu()
        if not herramientas:
            console.print("[red]Debes seleccionar al menos una herramienta.[/red]")
            continue

    prompt = construir_prompt(dominio, herramientas)
    inputs = {"messages": [{"role": "user", "content": prompt}]}

    mensajes_texto = []

    with console.status("[cyan]Analizando dominio...", spinner="dots"):
        for chunk in agent.stream(inputs, stream_mode="updates"):
            if "model" in chunk:
                for msg in chunk["model"]["messages"]:
                    contenido = getattr(msg, "content", "")
                    if isinstance(contenido, str) and len(contenido) > 200:
                        mensajes_texto.append(contenido)
                    elif isinstance(contenido, list):
                        for bloque in contenido:
                            if isinstance(bloque, dict) and bloque.get("type") == "text":
                                texto = bloque.get("text", "")
                                if len(texto) > 200:
                                    mensajes_texto.append(texto)

    resultado = max(mensajes_texto, key=len) if mensajes_texto else ""
    console.print(Markdown(resultado))

    # Score de riesgo
    try:
        with console.status("[cyan]Calculando score de riesgo...", spinner="dots"):
            reporte_estructurado = analizar_dominio_estructurado(dominio)
            score_data = calcular_score(reporte_estructurado)

        score_texto = Text()
        score_texto.append("\n🎯 SCORE DE RIESGO: ", style="bold")
        score_texto.append(
            f"{score_data['score']} puntos — {score_data['nivel']}",
            style=f"bold {score_data['color']}"
        )
        console.print(Panel(score_texto, border_style=score_data["color"], padding=(0, 2)))
    except Exception:
        pass

    exportar = questionary.confirm(
        "¿Deseas exportar el informe a PDF?",
        style=estilo_menu
    ).ask()

    if exportar:
        nombre_custom = questionary.text(
            "Nombre del fichero (Enter para nombre por defecto):",
            style=estilo_menu
        ).ask()

        with console.status("[cyan]Generando PDF...", spinner="dots"):
            fichero = generar_pdf(dominio, resultado, nombre_custom if nombre_custom else None)
        console.print(f"\n[bold green]✔ PDF guardado en: {fichero}[/bold green]\n")