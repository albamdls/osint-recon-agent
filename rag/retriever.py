from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def cargar_retriever(db_dir: str = "rag/chroma_db"):
    """Carga el vectorstore y devuelve un retriever."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory=db_dir,
        embedding_function=embeddings
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def consultar_conocimiento(pregunta: str) -> str:
    """
    Busca en la base de conocimiento y devuelve contexto relevante.
    Usado por el agente para contextualizar hallazgos.
    """
    retriever = cargar_retriever()
    docs = retriever.invoke(pregunta)
    
    if not docs:
        return "No se encontró información relevante."
    
    contexto = "\n\n".join([doc.page_content for doc in docs])
    return contexto

if __name__ == "__main__":
    # Test
    preguntas = [
        "¿Qué riesgo tiene no tener HSTS configurado?",
        "¿Qué son los Stealer Logs?",
        "¿Qué significa encontrar subdominios de staging expuestos?"
    ]
    for pregunta in preguntas:
        print(f"\n❓ {pregunta}")
        print(f"📚 {consultar_conocimiento(pregunta)[:200]}...")