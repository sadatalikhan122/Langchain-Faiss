
# 📄 LangChain Document Search with Hugging Face Embeddings & FAISS

A beginner-friendly **semantic document search** project built with Python, LangChain, Hugging Face embeddings, and FAISS.

The application loads a PDF, TXT, or DOCX document, divides its text into smaller chunks, converts those chunks into embeddings, and retrieves the most relevant passages for a question entered in the terminal.

> **Project Scope:** This project implements the retrieval component of a Retrieval-Augmented Generation (RAG) pipeline. It does not yet use an LLM to generate final answers.

## ✨ Features

- Load PDF, TXT, and DOCX documents.
- Validate file existence and readable content.
- Split documents into smaller overlapping chunks.
- Generate embeddings using Hugging Face models.
- Store vector embeddings using FAISS.
- Perform semantic similarity searches.
- Retrieve the top 3 relevant document chunks.
- Display document content and metadata.
- Interactive command-line question answering interface.
- Save FAISS vector indexes locally.

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| LangChain | Document processing and retrieval |
| Hugging Face | Text embedding generation |
| Sentence Transformers | Semantic embeddings |
| FAISS | Vector similarity search |
| PyPDFLoader | PDF document loading |
| TextLoader | TXT file loading |
| Docx2txtLoader | Word document loading |
| RecursiveCharacterTextSplitter | Text chunking |

## 🔄 Project Architecture

```text
PDF / TXT / DOCX Document
          |
          v
    Document Loader
          |
          v
      Text Splitting
   (500 character chunks)
   (100 character overlap)
          |
          v
   Hugging Face Embeddings
          |
          v
    Vector Embeddings
          |
          v
    FAISS Vector Store
          |
          v
      User Question
          |
          v
    Similarity Search
          |
          v
    Top 3 Relevant Chunks
          |
          v
      Display Results
```

## 📁 Project Structure

```text
LangChain-FAISS-Document-Retriever/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── documents/
│   └── sample.pdf
│
└── faiss_index/
```

## ⚙️ Installation

### Step 1: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```bash
pip install langchain-community langchain-text-splitters langchain-huggingface sentence-transformers faiss-cpu pypdf docx2txt
```

## 📄 Document Loading

The application supports multiple document formats.

```python
def load_document(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {path}"
        )

    extension = path.suffix.lower()

    if extension == ".pdf":
        loader = PyPDFLoader(str(path))

    elif extension == ".txt":
        loader = TextLoader(
            str(path),
            encoding="utf-8"
        )

    elif extension == ".docx":
        loader = Docx2txtLoader(str(path))

    else:
        raise ValueError(
            "Supported formats: PDF, TXT, DOCX"
        )

    return loader.load()
```

## ✂️ Text Splitting

Large documents are divided into smaller chunks using RecursiveCharacterTextSplitter.

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)
```

**Explanation:**

- `chunk_size=500`: Maximum target chunk length is 500 characters.
- `chunk_overlap=100`: Adjacent chunks can share 100 characters.
- Chunking helps with document retrieval and semantic search.

## 🧠 Hugging Face Embeddings

The project uses a pre-trained sentence transformer model.

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

### Embedding Model

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

This model converts text into numerical vectors that represent semantic meaning.

The model generates **384-dimensional embeddings**.

These embeddings help compare the similarity between user questions and document content.

## 🗄️ FAISS Vector Database

FAISS is used to store and search document embeddings.

```python
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

vector_store.save_local("faiss_index")
```

FAISS supports efficient vector similarity searching.

## 🔎 Document Retriever

The retriever searches for relevant chunks based on the user's question.

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
```

The parameter `k=3` means the retriever returns the three most relevant document chunks.

### Retrieve Documents

```python
results = retriever.invoke(question)

for i, doc in enumerate(results, start=1):

    print(f"\n--- Result {i} ---")

    print(
        f"Source: {doc.metadata.get('source', 'Unknown')}"
    )

    print(
        f"Page: {doc.metadata.get('page', 'N/A')}"
    )

    print(doc.page_content)
```

## ▶️ How to Run

### Step 1: Update Document Path

```python
FILE_PATH = r"C:\path\to\your\document.pdf"
```

Or use a relative path:

```python
FILE_PATH = "documents/sample.pdf"
```

### Step 2: Execute the Program

```bash
python main.py
```

### Step 3: Ask Questions

Example:

```text
Loading document...

Loaded 2 document page(s).

Created 8 chunks.

Loading embedding model...

Creating FAISS index...

FAISS index saved.

Ask a question about your document:
What skills are mentioned?

Relevant document content:

--- Result 1 ---
Source: documents/sample.pdf
Page: 0

[Relevant passage from the document]
```

*This is an illustrative output. Actual results depend on the selected document.*

## 🧠 Concepts Learned

Through this project, I developed practical understanding of:

- Python file handling
- LangChain document loaders
- PDF and DOCX processing
- Text preprocessing
- Recursive text splitting
- Chunk size and chunk overlap
- Hugging Face embedding models
- Sentence Transformers
- Vector embeddings
- FAISS vector databases
- Semantic similarity search
- LangChain retrievers
- Local vector index storage
- Fundamentals of RAG architecture

## ⚠️ Current Limitations

- The application retrieves document passages but does not generate answers using an LLM.
- Scanned PDF files may require OCR.
- The FAISS index is recreated on every execution.
- Only one document path is processed per run.
- Private documents and generated indexes should not be uploaded to public repositories.

### Recommended .gitignore

```gitignore
.venv/
__pycache__/
*.pyc
documents/
faiss_index/
```

## 🚀 Future Improvements

- Integrate Ollama with Llama 3.2.
- Build a complete RAG question-answering chatbot.
- Connect retrieved documents with an LLM.
- Add conversational memory.
- Support multiple document uploads.
- Implement a FastAPI backend.
- Create an HTML and JavaScript frontend.
- Deploy the application using AWS.
- Add retrieval quality evaluation.

## 👨‍💻 Author

**Sadat Ali Khan**

**GitHub:**  
https://github.com/sadatalikhan122

**LinkedIn:**  
https://www.linkedin.com/in/sadat-ali-khan-90ba701a0/

## 📌 Project Purpose

This project was developed as part of my Machine Learning, Natural Language Processing, and LLM Engineering learning journey.

The primary goal was to gain hands-on experience with document loading, text chunking, embedding models, vector databases, and semantic retrieval using LangChain.

It demonstrates the core building blocks required to develop Retrieval-Augmented Generation (RAG) applications.
