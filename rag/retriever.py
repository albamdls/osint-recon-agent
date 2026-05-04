from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def load_retriever(db_dir: str = "rag/chroma_db"):
    """Loads the vectorstore and returns a retriever."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory=db_dir,
        embedding_function=embeddings
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def query_knowledge(question: str) -> str:
    """
    Searches the knowledge base and returns relevant context.
    Used by the agent to contextualize findings.
    """
    retriever = load_retriever()
    docs = retriever.invoke(question)
    
    if not docs:
        return "No relevant information found."
    
    context = "\n\n".join([doc.page_content for doc in docs])
    return context

if __name__ == "__main__":
    # Test
    questions = [
        "What risk is there if HSTS is not configured?",
        "What are Stealer Logs?",
        "What does it mean to find exposed staging subdomains?"
    ]
    for question in questions:
        print(f"\n❓ {question}")
        print(f"📚 {query_knowledge(question)[:200]}...")