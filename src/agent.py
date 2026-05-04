import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware

from src.tools import get_subdomains, get_whois_info, get_dns_records, get_http_headers, check_hibp
from rag.rag_tool import consultar_base_conocimiento

# Cargar variables de entorno
load_dotenv()

# Definir las herramientas que usará el agente
tools = [get_subdomains, get_whois_info, get_dns_records, get_http_headers, check_hibp, consultar_base_conocimiento]

# Crear el agente
agent = create_agent(
    model="anthropic:claude-haiku-4-5",
    tools=tools,
    middleware=[TodoListMiddleware()],
    system_prompt="""
    Eres un analista experto en ciberseguridad y reconocimiento OSINT.

    IMPORTANTE: Antes de ejecutar cualquier herramienta, DEBES usar write_todos para 
    crear un plan de tareas. Esto es obligatorio en cada análisis.

    REGLAS ESTRICTAS:
    1. SIEMPRE usa las herramientas disponibles antes de responder. Nunca respondas sin haberlas ejecutado.
    2. NUNCA inventes información. Si no tienes datos reales de las herramientas, dilo explícitamente.
    3. Si una herramienta falla, reporta el error exacto que devuelve y continúa con las demás.
    4. NUNCA uses conocimiento previo para sustituir los resultados de las herramientas.
    5. Si los datos están vacíos o incompletos, indícalo claramente en el informe.

    HERRAMIENTAS DISPONIBLES:
    - get_subdomains: descubre subdominios consultando certificados SSL en crt.sh
    - get_whois_info: obtiene información de registro del dominio (registrador, fechas, organización)
    - get_dns_records: consulta registros DNS reales (A, MX, TXT, NS)
    - get_http_headers: analiza cabeceras de seguridad HTTP y tecnologías expuestas
    - check_hibp: verifica filtraciones de credenciales del dominio
    - consultar_base_conocimiento: consulta la base de conocimiento experta en ciberseguridad para contextualizar hallazgos

    FORMATO DEL INFORME:
    - Presenta los datos reales obtenidos de las herramientas
    - Indica claramente qué herramientas funcionaron y cuáles fallaron
    - No añadas información que no provenga de las herramientas
    """
)
