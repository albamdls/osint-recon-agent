from langchain.tools import tool
from rag.retriever import consultar_conocimiento

@tool
def consultar_base_conocimiento(pregunta: str) -> str:
    """
    Consulta la base de conocimiento experta en ciberseguridad.
    Úsala cuando necesites contexto sobre:
    - Severidad de cabeceras HTTP ausentes
    - Qué significa un tipo de filtración de datos
    - Riesgo de subdominios expuestos
    - Vulnerabilidades OWASP
    - Interpretación de registros DNS
    """
    return consultar_conocimiento(pregunta)