import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def create_knowledge_base(data_dir: str = "rag/data", db_dir: str = "rag/chroma_db"):
    """Indexes markdown documents into ChromaDB."""
    
    print("📚 Loading documents...")
    loader = DirectoryLoader(
        data_dir,
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    print(f"✅ {len(documents)} documents loaded")

    print("✂️ Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ {len(chunks)} chunks created")

    print("🔢 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("💾 Indexing into ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir
    )
    print(f"✅ Knowledge base created at {db_dir}")
    return vectorstore

if __name__ == "__main__":
    create_knowledge_base()