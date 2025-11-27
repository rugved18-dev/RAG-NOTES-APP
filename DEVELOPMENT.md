# Development Guide - Chat with Your Notes

## Project Overview

This guide covers the architecture, code structure, and development workflow for the Chat with Your Notes RAG application.

## Architecture

### High-Level Flow

```
User Input
    ↓
PDF Upload → PDF Processor → ChromaDB Vector Store
    ↓
User Query → Embeddings → Vector Search (Retrieval)
    ↓
Retrieved Context + Memory → LangChain RAG Chain
    ↓
GPT-3.5-Turbo → Response with Citations
    ↓
Streamlit UI Display
```

## Component Details

### 1. PDF Processor (`pdf_processor.py`)

**Purpose**: Loads and chunks PDF documents for embedding.

**Key Functions**:
- `load_pdf(file_path)`: Extracts text from PDF with page metadata
- `chunk_documents(documents)`: Splits text into overlapping chunks
- `process_pdf_file(file_path)`: Complete pipeline

**Key Features**:
- Preserves page numbers for citations
- Overlapping chunks for context preservation
- Metadata tagging for source tracking

**Configuration Parameters**:
```python
chunk_size = 1000        # Characters per chunk
chunk_overlap = 200      # Overlap between chunks
```

**Example Usage**:
```python
from app.pdf_processor import process_pdf_file

documents, file_name = process_pdf_file("textbook.pdf")
# Returns: (List[Document], "textbook.pdf")
```

### 2. RAG Chain (`rag_chain.py`)

**Purpose**: Manages vector store, retrieval, and LLM interactions.

**Key Classes**:
- `RAGChain`: Main class for RAG operations

**Key Methods**:
- `__init__()`: Initialize embeddings, LLM, and vector store
- `add_documents()`: Add chunked documents to ChromaDB
- `load_existing_store()`: Load previously created vector store
- `query()`: Process user questions and return answers with sources
- `set_temperature()`: Adjust model creativity
- `clear_memory()`: Reset conversation history

**Memory Management**:
- Uses `ConversationBufferMemory` from LangChain
- Stores last 4 messages in prompt context
- Allows coherent follow-up questions

**Source Citations**:
- Extracts source metadata from retrieved documents
- Returns file name and page number with each answer
- Prevents hallucination by grounding in actual documents

**Example Usage**:
```python
from app.rag_chain import RAGChain

# Initialize
rag = RAGChain(api_key="sk-...", temperature=0.7)

# Add documents
rag.add_documents(chunked_docs, "chapter1.pdf")

# Query
response = rag.query("What is photosynthesis?")
# Returns: {"answer": "...", "sources": [...]}
```

### 3. Streamlit UI (`app.py`)

**Purpose**: Provides user interface and state management.

**Key Sections**:
1. **Sidebar Settings**
   - API key input with validation
   - PDF upload with progress tracking
   - Document statistics display
   - Temperature slider
   - Clear chat button

2. **Main Chat Interface**
   - Message history display
   - Chat input box
   - Real-time response streaming
   - Source citations display

**Session State Management**:
```python
st.session_state.rag_chain          # RAG chain instance
st.session_state.chat_history       # Message history
st.session_state.uploaded_files     # Loaded document metadata
st.session_state.api_key_valid      # API key validation flag
```

## Development Workflow

### 1. Setting Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install black pylint pytest
```

### 2. Running Locally

```bash
# Set API key
export OPENAI_API_KEY="sk-..."  # On Windows: set OPENAI_API_KEY=...

# Run app
streamlit run app/app.py

# Access at http://localhost:8501
```

### 3. Code Structure Guidelines

**Naming Conventions**:
- Classes: PascalCase (e.g., `RAGChain`)
- Functions: snake_case (e.g., `load_pdf`)
- Constants: UPPER_SNAKE_CASE
- Private methods: prefix with `_` (e.g., `_format_chat_history`)

**Module Organization**:
```
app/
├── __init__.py           # Package initialization
├── app.py               # Main Streamlit app (UI layer)
├── pdf_processor.py     # Document processing (Data layer)
└── rag_chain.py        # RAG logic (Business logic layer)
```

## Key Technologies & APIs

### OpenAI

**Embedding Model**: `text-embedding-3-small`
- Cost: ~$0.0001 per 1K tokens
- Dimension: 512
- Used for: Converting text to vectors

**Chat Model**: `gpt-3.5-turbo`
- Cost: ~$0.0005-$0.002 per 1K tokens
- Used for: Generating responses

**API Calls**:
```python
# In rag_chain.py
self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
self.llm = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo")
```

### ChromaDB

**Vector Database**: Persistent storage of embeddings
- Default location: `.chroma/` directory
- Auto-persisted after each operation
- Supports incremental updates

**Collection Management**:
```python
# Create collection
vector_store = Chroma.from_documents(documents, embeddings)

# Load existing
vector_store = Chroma(persist_directory=path, embedding_function=emb)

# Retrieve similar documents
retriever = vector_store.as_retriever(search_kwargs={"k": 4})
```

### LangChain

**Key Components Used**:
1. **Text Splitter**: `RecursiveCharacterTextSplitter`
2. **Vector Store Integration**: `Chroma`
3. **Memory**: `ConversationBufferMemory`
4. **Chain**: `RetrievalQA`
5. **Prompts**: `PromptTemplate`

## Customization Guide

### 1. Change LLM Model

```python
# In rag_chain.py, __init__ method
self.llm = ChatOpenAI(
    api_key=api_key,
    temperature=temperature,
    model="gpt-4"  # Change here
)
```

### 2. Adjust Chunk Size

```python
# In pdf_processor.py, chunk_documents function
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,    # Increase for larger chunks
    chunk_overlap=400,  # Increase for more overlap
)
```

### 3. Change Retrieval Strategy

```python
# In rag_chain.py, add_documents method
self.retriever = self.vector_store.as_retriever(
    search_kwargs={"k": 6}  # Retrieve more chunks
)
```

### 4. Modify Chat Prompt

```python
# In rag_chain.py, query method
prompt_template = """Your custom prompt here...
{context}
{chat_history}
{question}"""
```

### 5. Add Local LLM Support

```python
# Instead of ChatOpenAI, use:
from langchain.llms import Ollama
self.llm = Ollama(model="llama2")
```

## Error Handling

### Common Issues & Solutions

**Issue**: Import errors after installation
```
Solution: Ensure virtual environment is activated
and requirements.txt is installed correctly
```

**Issue**: ChromaDB connection errors
```
Solution: Delete .chroma/ directory and re-upload documents
```

**Issue**: Slow embedding generation
```
Solution: Reduce chunk_size or use smaller documents
```

**Issue**: Low quality answers
```
Solution: Increase retrieval chunks (k=6), adjust temperature
```

## Testing

### Manual Testing Checklist

- [ ] API key validation works
- [ ] PDF upload and processing works
- [ ] Multiple files can be uploaded
- [ ] Chat history is preserved
- [ ] Sources are cited correctly
- [ ] Clear chat button works
- [ ] Temperature slider affects responses
- [ ] Follow-up questions work with context
- [ ] Previous documents persist after page reload

### Unit Testing (Future)

```python
# example_test.py
import pytest
from app.pdf_processor import chunk_documents
from app.rag_chain import RAGChain

def test_chunk_documents():
    # Test document chunking
    pass

def test_rag_chain_initialization():
    # Test RAG chain setup
    pass
```

## Performance Optimization

### 1. Batch Document Processing
```python
# Process multiple documents at once
for file in files:
    chunks, name = process_pdf_file(file)
    rag.add_documents(chunks, name)
```

### 2. ChromaDB Persistence
```python
# Vector store persists automatically
# Loading existing store is faster than re-embedding
rag.load_existing_store()  # Fast reload
```

### 3. Retrieval Optimization
```python
# Balance between relevance and speed
retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}  # 4 is optimal
)
```

## Deployment

### Prerequisites
- Python 3.8+
- OpenAI API key
- ~500MB storage for ChromaDB

### Cloud Deployment Options

**Option 1: Streamlit Cloud (Recommended)**
```bash
# 1. Push to GitHub
git push origin main

# 2. Deploy on Streamlit Cloud
# Visit: https://share.streamlit.io
# Connect GitHub repo and deploy
```

**Option 2: Docker**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app/app.py"]
```

**Option 3: AWS/Azure/GCP**
- Use Docker image or native Python deployment
- Ensure persistent storage for ChromaDB (`.chroma/`)
- Set environment variables for API key

## Contributing

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions

### Commit Messages
```
feat: Add new feature
fix: Fix bug
docs: Update documentation
refactor: Reorganize code
```

### Pull Request Process
1. Create feature branch
2. Make changes with clear commits
3. Test thoroughly
4. Submit PR with description

## Troubleshooting Development

### Virtual Environment Issues
```bash
# Recreate venv if corrupted
rm -r venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Dependency Conflicts
```bash
# Update all dependencies
pip install --upgrade -r requirements.txt

# Check for conflicts
pip check
```

### Streamlit Caching Issues
```bash
# Clear Streamlit cache
streamlit cache clear
```

## Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [RAG Patterns](https://docs.anthropic.com/claude/docs/retrieval-augmented-generation)

---

For questions or issues, refer to the main README.md or check the GitHub issues section.
