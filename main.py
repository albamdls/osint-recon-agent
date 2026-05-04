from src.agent import agent
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich.spinner import Spinner
from pyfiglet import figlet_format
from reports.pdf_generator import generate_pdf
import questionary
import json
from questionary import Style
from src.structured_agent import analyze_domain_structured
from src.scorer import calculate_score

console = Console()

menu_style = Style([
    ('qmark', 'fg:cyan bold'),
    ('question', 'fg:white bold'),
    ('answer', 'fg:cyan bold'),
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan bold'),
    ('selected', 'fg:green bold'),
    ('separator', 'fg:cyan'),
    ('instruction', 'fg:white'),
])

def show_banner():
    banner = figlet_format("OSINT AI CLI", font="doom")
    title = Text(banner, style="bold green")
    subtitle = Text()
    subtitle.append("[ ", style="green")
    subtitle.append("AI-Powered OSINT Reconnaissance Tool", style="bold white")
    subtitle.append(" ]", style="green")
    author = Text()
    author.append("[ ", style="green")
    author.append("Developed by ", style="dim white")
    author.append("Alba Mora", style="bold green")
    author.append(" · Final Project AI Automation 2026", style="dim white")
    author.append(" ]", style="green")
    disclaimer = Text(justify="center")
    disclaimer.append("⚠  ", style="bold yellow")
    disclaimer.append("FOR ACADEMIC AND EDUCATIONAL USE ONLY", style="bold yellow")
    disclaimer.append("  ⚠", style="bold yellow")
    disclaimer.append("\n   This tool is designed exclusively for learning purposes.", style="dim yellow")
    console.print(title, justify="center")
    console.print(subtitle, justify="center")
    console.print(author, justify="center")
    console.print()
    console.print(Panel(disclaimer, border_style="yellow", padding=(0, 2)), justify="center")
    console.print()

def show_menu():
    return questionary.select(
        "What would you like to do?",
        choices=[
            questionary.Choice("⚡ Full domain analysis", value=1),
            questionary.Choice("🔧 Custom analysis", value=2),
            questionary.Choice("🔍 Scan secrets in GitHub", value=3),
            questionary.Choice("❌ Exit", value=4),
        ],
        style=menu_style
    ).ask()

def show_submenu():
    return questionary.checkbox(
        "Select tools to use:",
        choices=[
            questionary.Choice("🌐 Subdomains (crt.sh)", value="Subdomains (crt.sh)"),
            questionary.Choice("📋 WHOIS", value="WHOIS"),
            questionary.Choice("🔗 DNS Records", value="DNS Records"),
            questionary.Choice("🔒 HTTP Headers", value="HTTP Headers"),
            questionary.Choice("⚠️ Credential Leaks (LeakCheck)", value="Credential Leaks (LeakCheck)"),
        ],
        style=menu_style
    ).ask()

def build_prompt(domain, tools):
    if tools is None:
        return f"Perform a complete OSINT analysis of the domain {domain} using all available tools."
    names = {
        "Subdomains (crt.sh)": "get_subdomains",
        "WHOIS": "get_whois_info",
        "DNS Records": "get_dns_records",
        "HTTP Headers": "get_http_headers",
        "Credential Leaks (LeakCheck)": "check_hibp"
    }
    selected_tools = [names[t] for t in tools]
    tools_str = ", ".join(selected_tools)
    return f"Analyze the domain {domain} using ONLY these tools: {tools_str}. Do not use any other tool."

while True:
    show_banner()
    op = show_menu()

    if op == 4:
        console.print("\n[bold green]Goodbye, agent. ⚡[/bold green]\n")
        break

    elif op == 3:
        target = questionary.text(
            "Enter GitHub user or organization:",
            style=menu_style
        ).ask()

        if target:
            from src.secrets_scanner import scan_github_secrets
            with console.status("[cyan]Scanning repositories...", spinner="dots"):
                scan_result = scan_github_secrets.invoke({"target": target})
            console.print(Markdown(scan_result))
        else:
            console.print("[red]Invalid user.[/red]")
        continue

    domain = questionary.text(
        "Enter the domain to analyze:",
        style=menu_style
    ).ask()

    if not domain:
        console.print("[red]Invalid domain.[/red]")
        continue

    tools = None
    if op == 2:
        tools = show_submenu()
        if not tools:
            console.print("[red]Please select at least one tool.[/red]")
            continue

    prompt = build_prompt(domain, tools)
    inputs = {"messages": [{"role": "user", "content": prompt}]}

    text_messages = []

    with console.status("[cyan]Analyzing domain...", spinner="dots"):
        for chunk in agent.stream(inputs, stream_mode="updates"):
            if "model" in chunk:
                for msg in chunk["model"]["messages"]:
                    content = getattr(msg, "content", "")
                    if isinstance(content, str) and len(content) > 200:
                        text_messages.append(content)
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                text = block.get("text", "")
                                if len(text) > 200:
                                    text_messages.append(text)

    result = max(text_messages, key=len) if text_messages else ""
    console.print(Markdown(result))

    try:
        with console.status("[cyan]Calculating risk score...", spinner="dots"):
            structured_report = analyze_domain_structured(domain)
            score_data = calculate_score(structured_report)

        score_text = Text()
        score_text.append("\n🎯 RISK SCORE: ", style="bold")
        score_text.append(
            f"{score_data['score']} points — {score_data['level']}",
            style=f"bold {score_data['color']}"
        )
        console.print(Panel(score_text, border_style=score_data["color"], padding=(0, 2)))
    except Exception:
        pass

    export = questionary.confirm(
        "Would you like to export the report to PDF?",
        style=menu_style
    ).ask()

    if export:
        custom_name = questionary.text(
            "Filename (press Enter for default):",
            style=menu_style
        ).ask()

        with console.status("[cyan]Generating PDF...", spinner="dots"):
            file = generate_pdf(domain, result, custom_name if custom_name else None)
        console.print(f"\n[bold green]✔ PDF saved at: {file}[/bold green]\n")