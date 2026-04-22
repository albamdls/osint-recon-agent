import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from src.tools import get_subdomains, get_whois_info

# Cargar variables de entorno
load_dotenv()

# Definir las herramientas que usará el agente
tools = [get_subdomains, get_whois_info]

# Crear el agente
agent = create_agent(
    model="anthropic:claude-haiku-4-5",
    tools=tools,
    system_prompt="""
        Eres un asistente experto en reconocimiento OSINT. Dado un dominio,
        usas las herramientas disponibles para descubrir subdominios e información de registro.
        """
)

if __name__ == "__main__":
    inputs = {"messages": [{"role": "user", "content":"Analiza el dominio github.com"}]}
    for chunk in agent.stream(inputs, stream_mode="updates"):
        print(chunk)