
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# 1. Set your document path here
FILE_PATH = r"C:\Users\sadat ali khan\Desktop\langchain\Sadat-Ali-Khan-CV (1).pdf"


def load_document(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        loader = PyPDFLoader(str(path))
    elif extension == ".txt":
        loader = TextLoader(str(path), encoding="utf-8")
    elif extension == ".docx":
        loader = Docx2txtLoader(str(path))
    else:
        raise ValueError("Supported formats: PDF, TXT, DOCX")

    return loader.load()


def main():
    # 2. Load document
    print("Loading document...")
    documents = load_document(FILE_PATH)

    if not any(doc.page_content.strip() for doc in documents):
        raise ValueError(
            "No text found. If this is a scanned PDF, use OCR first."
        )

    print(f"Loaded {len(documents)} document page(s).")

    # 3. Split into small chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    # 4. Convert chunks into embeddings
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 5. Store vectors in FAISS
    print("Creating FAISS index...")
    vector_store = FAISS.from_documents(chunks, embeddings)

     
    # Save the index for later use
    print(str(vector_store))
    vector_store.save_local("faiss_index")
    print("FAISS index saved.")

    retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
    # 6. Search your document
    while True:
        question = input(
            "\nAsk a question about your document "
            "(or type 'exit'): "
        ).strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        results = retriever

        print("\nRelevant document content:")

        for i, doc in enumerate(results, start=1):
            print(f"\n--- Result {i} ---")
            print(f"Source: {doc.metadata.get('source', 'Unknown')}")
            print(f"Page: {doc.metadata.get('page', 'N/A')}")
            print(doc.page_content)


if __name__ == "__main__":
    main()
