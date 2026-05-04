import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def crear_base_conocimiento(data_dir: str = "rag/data", db_dir: str = "rag/chroma_db"):
    """Indexa los documentos markdown en ChromaDB."""
    
    print("📚 Cargando documentos...")
    loader = DirectoryLoader(
        data_dir,
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documentos = loader.load()
    print(f"✅ {len(documentos)} documentos cargados")

    print("✂️ Dividiendo en chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documentos)
    print(f"✅ {len(chunks)} chunks creados")

    print("🔢 Creando embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("💾 Indexando en ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir
    )
    print(f"✅ Base de conocimiento creada en {db_dir}")
    return vectorstore

if __name__ == "__main__":
    crear_base_conocimiento()