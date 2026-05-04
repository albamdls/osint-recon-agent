from langchain.tools import tool
from rag.retriever import query_knowledge

@tool
def query_knowledge_base(question: str) -> str:
    """
    Queries the cybersecurity expert knowledge base.
    Use it when you need context about:
    - Severity of missing HTTP headers
    - Meaning of a type of data breach
    - Risk of exposed subdomains
    - OWASP vulnerabilities
    - Interpretation of DNS records
    """
    return query_knowledge(question)