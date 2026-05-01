import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from src.schemas import ReconReport, WhoisInfo, DNSInfo, HeadersInfo, FiltracionesInfo
from src.tools import get_subdomains, get_whois_info, get_dns_records, get_http_headers, check_hibp
from datetime import datetime

load_dotenv()

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
llm_structured = llm.with_structured_output(ReconReport)

def analizar_dominio_estructurado(dominio: str) -> ReconReport:
    """
    Ejecuta las herramientas OSINT y devuelve un informe estructurado
    usando Pydantic para garantizar el formato de salida.
    """
    # 1. Ejecutar herramientas directamente
    resultados = {}
    herramientas_fallidas = []

    try:
        resultados["whois"] = get_whois_info.invoke({"domain": dominio})
    except Exception as e:
        herramientas_fallidas.append(f"whois: {str(e)}")

    try:
        resultados["dns"] = get_dns_records.invoke({"domain": dominio})
    except Exception as e:
        herramientas_fallidas.append(f"dns: {str(e)}")

    try:
        resultados["subdominios"] = get_subdomains.invoke({"domain": dominio})
    except Exception as e:
        herramientas_fallidas.append(f"subdominios: {str(e)}")

    try:
        resultados["headers"] = get_http_headers.invoke({"domain": dominio})
    except Exception as e:
        herramientas_fallidas.append(f"headers: {str(e)}")

    try:
        resultados["filtraciones"] = check_hibp.invoke({"domain": dominio})
    except Exception as e:
        herramientas_fallidas.append(f"filtraciones: {str(e)}")

    # 2. Pedir al LLM que estructure los datos
    prompt = f"""
    Analiza los siguientes datos OSINT del dominio {dominio} y devuelve un informe estructurado.
    
    Datos recopilados:
    {resultados}
    
    Herramientas fallidas: {herramientas_fallidas}
    
    Rellena todos los campos del schema con la información disponible.
    Para nivel_riesgo usa: BAJO, MEDIO, ALTO o CRÍTICO.
    Para resumen escribe 2-3 frases resumiendo los hallazgos más importantes.
    Para recomendaciones lista las 3-5 más importantes.
    """

    reporte = llm_structured.invoke(prompt)
    reporte.dominio = dominio
    reporte.fecha_analisis = datetime.now().strftime("%d/%m/%Y %H:%M")
    reporte.herramientas_fallidas = herramientas_fallidas

    return reporte