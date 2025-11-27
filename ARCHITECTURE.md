# Architecture Diagram - Chat with Your Notes RAG

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      STREAMLIT UI LAYER                          │
│                       (app/app.py)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐      ┌──────────────────┐                 │
│  │  Sidebar Panel   │      │  Main Chat Area  │                 │
│  ├──────────────────┤      ├──────────────────┤                 │
│  │ • API Key Input  │      │ • Message List   │                 │
│  │ • PDF Uploader   │      │ • Chat Input     │                 │
│  │ • File List      │      │ • Source Display │                 │
│  │ • Settings       │      │ • Loading State  │                 │
│  │ • Clear Button   │      │                  │                 │
│  └──────────────────┘      └──────────────────┘                 │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   APPLICATION LOGIC LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐      ┌──────────────────┐                  │
│  │ PDF Processor   │      │   RAG Chain      │                  │
│  │ (pdf_          │      │ (rag_chain.py)   │                  │
│  │  processor.py) │      │                  │                  │
│  ├─────────────────┤      ├──────────────────┤                  │
│  │ • Load PDF      │      │ • LLM Init       │                  │
│  │ • Extract Text  │      │ • Memory Mgmt    │                  │
│  │ • Chunk Text    │      │ • Retrieval      │                  │
│  │ • Add Metadata  │      │ • Query Process  │                  │
│  │ • Create Docs   │      │ • Source Extract │                  │
│  └─────────────────┘      └──────────────────┘                  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
         │                              │
         │ Chunked                      │ Query
         │ Documents                    │ Results
         ▼                              ▼
┌──────────────────────────────────────────────────────────┐
│              VECTOR STORE & EMBEDDINGS LAYER             │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────┐          ┌──────────────────┐        │
│  │  ChromaDB      │◄────────►│ OpenAI API       │        │
│  │  Vector Store  │          │ (Embeddings)     │        │
│  ├────────────────┤          └──────────────────┘        │
│  │ • Collections  │                                       │
│  │ • Embeddings   │          Generate vectors for:        │
│  │ • Metadata     │          • PDFs (on upload)           │
│  │ • Similarity   │          • Questions (on query)       │
│  │  Search        │          • Comparison                 │
│  └────────────────┘                                       │
│                                                            │
│  Stored on Disk: .chroma/ directory                      │
└──────────────────────────────────────────────────────────┘
         │
         │ Retrieved Context
         │ + Query
         ▼
┌──────────────────────────────────────────────────────────┐
│          LANGUAGE MODEL & RESPONSE LAYER                 │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────────────────────────────────┐          │
│  │ OpenAI GPT-3.5-Turbo                       │          │
│  ├────────────────────────────────────────────┤          │
│  │ INPUT:                                     │          │
│  │  • Retrieved chunks (top 4)                │          │
│  │  • Conversation history (last 4 messages) │          │
│  │  • Custom prompt with citation rules      │          │
│  │  • User question                          │          │
│  │                                            │          │
│  │ OUTPUT:                                    │          │
│  │  • Answer text                            │          │
│  │  • Source information                     │          │
│  │  • Page citations                         │          │
│  └────────────────────────────────────────────┘          │
│                                                            │
└──────────────────────────────────────────────────────────┘
         │
         │ Response with Sources
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DISPLAY & STORAGE                             │
├─────────────────────────────────────────────────────────────────┤
│  • Format answer with Markdown                                   │
│  • Extract and display sources                                   │
│  • Add to chat history (Streamlit session state)                 │
│  • Store in memory (LangChain buffer)                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
USER UPLOAD PDF
    │
    ▼
┌─────────────────────┐
│ Save to /uploads    │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ PDF Processor       │──► Extract text + page metadata
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Chunk Documents     │──► Split into 1000-char chunks
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Generate Embeddings │──► OpenAI Embedding API
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Store in ChromaDB   │──► Persist to .chroma/
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Display Success     │──► Show to user
└─────────────────────┘


USER ASKS QUESTION
    │
    ▼
┌─────────────────────┐
│ Generate Embedding  │──► OpenAI Embedding API
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Vector Search       │──► Find top 4 similar chunks
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Load Chat History   │──► Last 4 messages from memory
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Build Prompt        │──► Combine context + history + query
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Send to GPT-3.5     │──► OpenAI Chat API
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Parse Response      │──► Extract answer + sources
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Format Display      │──► Markdown + citations
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Update Memory       │──► Add to conversation buffer
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ Show to User        │──► Answer + sources in chat
└─────────────────────┘
```

---

## Component Interaction Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                                                               │
│    Streamlit App (UI)                                        │
│    ├─ Session State Management                              │
│    ├─ File Upload Handling                                  │
│    └─ Chat Message Display                                  │
│                                                               │
│          │                          │                       │
│          │ PDF Files                │ User Questions         │
│          ▼                          ▼                       │
│    ┌───────────────┐          ┌────────────────┐           │
│    │ PDF Processor │          │  RAG Chain     │           │
│    │               │          │                │           │
│    │ • Load PDF    │          │ • Query Parser │           │
│    │ • Chunk Text  │          │ • Retriever    │           │
│    │ • Add Meta    │          │ • LLM Caller   │           │
│    └───────────────┘          │ • Memory Mgr   │           │
│          │                    │ • Citation Gen │           │
│          │ Chunks             │ • Response     │           │
│          │ + Metadata         └────────────────┘           │
│          │                          │                       │
│          │                          │ Top 4 Chunks          │
│          ▼                          │ + History             │
│    ┌──────────────────────────────┐│                        │
│    │                              ││                        │
│    │     ChromaDB                 ││                        │
│    │  Vector Store                ││                        │
│    │                              ││                        │
│    │ • Document                   ││                        │
│    │   Embeddings                 ││                        │
│    │ • Similarity Search          ││                        │
│    │ • Metadata Lookup            ││                        │
│    │                              ││                        │
│    └──────────────────────────────┘│                        │
│          │                         │                       │
│          │ Vector Storage          │ Similarity             │
│          │                         │ Scores                 │
│          ▼                         ▼                       │
│    .chroma/          ┌─────────────────────┐               │
│    (Disk)            │   OpenAI API        │               │
│                      │                     │               │
│                      │ • Embeddings API    │               │
│                      │ • Chat API          │               │
│                      │ • Temperature       │               │
│                      │   Control           │               │
│                      │                     │               │
│                      │ Returns: Answer +   │               │
│                      │ Sources             │               │
│                      └─────────────────────┘               │
│          │                         │                       │
│          │ Memory Storage          │ Response + Meta       │
│          │                         │                       │
│          ▼                         ▼                       │
│    ┌──────────────────────────────┐                        │
│    │                              │                        │
│    │  Session State (UI)          │                        │
│    │                              │                        │
│    │ • Chat History               │                        │
│    │ • Uploaded Files             │                        │
│    │ • Settings                   │                        │
│    │                              │                        │
│    └──────────────────────────────┘                        │
│                │                                           │
│                │ Display to User                           │
│                ▼                                           │
│    ┌──────────────────────────────┐                        │
│    │  Chat Interface Rendered     │                        │
│    │  • Message Bubbles           │                        │
│    │  • Source Citations          │                        │
│    │  • Loading States            │                        │
│    │  • Error Messages            │                        │
│    └──────────────────────────────┘                        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Class & Method Structure

```
RAGChain (rag_chain.py)
├── __init__(api_key, temperature, chroma_db_path)
│   ├── Initialize embeddings (OpenAI)
│   ├── Initialize LLM (GPT-3.5-Turbo)
│   ├── Initialize vector store (ChromaDB)
│   └── Initialize memory (ConversationBufferMemory)
│
├── add_documents(documents, file_name)
│   ├── Create/update vector store with Chroma
│   ├── Persist to disk
│   └── Return success message
│
├── load_existing_store()
│   ├── Load previous ChromaDB if exists
│   └── Return loaded status
│
├── query(question)
│   ├── Retrieve top 4 similar chunks
│   ├── Load chat history
│   ├── Create prompt with context
│   ├── Call LLM with temperature
│   ├── Parse response and sources
│   ├── Add to memory
│   └── Return answer + sources
│
├── set_temperature(temperature)
│   └── Update LLM temperature
│
├── clear_memory()
│   └── Reset conversation history
│
└── get_collection_info()
    └── Return vector store statistics


PDF Processing Functions (pdf_processor.py)
├── load_pdf(file_path)
│   ├── Extract text from PDF
│   ├── Add page metadata
│   └── Return Document objects
│
├── chunk_documents(documents, chunk_size, overlap)
│   ├── Split text with overlap
│   ├── Preserve metadata
│   └── Return chunked documents
│
└── process_pdf_file(file_path)
    ├── Load PDF
    ├── Chunk documents
    └── Return complete pipeline result


Streamlit App (app.py)
├── Session State Management
│   ├── rag_chain instance
│   ├── chat_history list
│   ├── uploaded_files dict
│   └── api_key_valid bool
│
├── Sidebar Section
│   ├── API Key Input + Validation
│   ├── PDF Upload Handler
│   ├── Document Statistics
│   ├── Temperature Slider
│   └── Clear Chat Button
│
├── Main Chat Section
│   ├── Display Chat History
│   ├── Chat Input Box
│   ├── Query Handler
│   ├── Display Response
│   └── Display Sources
│
└── Custom CSS & Formatting
    ├── Layout styling
    ├── Message formatting
    └── Citation display
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────────────────┐
│         USER INTERFACE LAYER                     │
│  Streamlit (Web UI, Real-time updates)          │
└─────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│      APPLICATION LOGIC LAYER                    │
│  Python (PDF Processing, RAG Orchestration)     │
└─────────────────────────────────────────────────┘
         │
         ├─────────────────────────┬──────────────┐
         ▼                         ▼              ▼
┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐
│ VECTOR LAYER     │  │ LLM LAYER        │  │ PDF LAYER   │
│ ChromaDB         │  │ OpenAI API       │  │ PyPDF2      │
│ Embeddings       │  │ GPT-3.5-Turbo    │  │             │
└──────────────────┘  └──────────────────┘  └─────────────┘
         │                   │                      │
         └───────┬───────────┴──────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────┐
    │ EXTERNAL SERVICES            │
    │ OpenAI (API calls)           │
    │ Internet (HTTP requests)     │
    └──────────────────────────────┘
```

---

## Deployment Architecture (Optional)

```
┌────────────────────────────────────────────────────┐
│          CLOUD DEPLOYMENT OPTIONS                  │
├────────────────────────────────────────────────────┤
│                                                     │
│  Option 1: Streamlit Cloud (Easiest)              │
│  ┌──────────────────────────────────┐             │
│  │ streamlit.app hosting            │             │
│  │ Git integration                  │             │
│  │ Auto-deploy on push              │             │
│  │ Custom domain support            │             │
│  └──────────────────────────────────┘             │
│                                                     │
│  Option 2: Docker + Cloud (AWS/Azure/GCP)        │
│  ┌──────────────────────────────────┐             │
│  │ Dockerfile packaging             │             │
│  │ Container registry               │             │
│  │ Orchestration                    │             │
│  │ Auto-scaling                     │             │
│  └──────────────────────────────────┘             │
│                                                     │
│  Option 3: Traditional Server                     │
│  ┌──────────────────────────────────┐             │
│  │ Linux server + Nginx             │             │
│  │ Gunicorn runner                  │             │
│  │ Supervisor/systemd               │             │
│  │ SSL certificate                  │             │
│  └──────────────────────────────────┘             │
│                                                     │
└────────────────────────────────────────────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Easiest  │      │ Scalable │      │ Control  │
    └──────────┘      └──────────┘      └──────────┘
```

---

## State Management Flow

```
COMPONENT: Session State (Streamlit)

session_state = {
    "rag_chain": RAGChain instance,
    "chat_history": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "...", "sources": [...]},
        ...
    ],
    "uploaded_files": {
        "chapter1.pdf": {"pages": 45, "chunks": 89},
        "chapter2.pdf": {"pages": 38, "chunks": 76},
    },
    "api_key_valid": True/False
}


MEMORY MANAGEMENT: LangChain ConversationBufferMemory

memory = {
    "messages": [
        HumanMessage(content="Question 1"),
        AIMessage(content="Answer 1"),
        HumanMessage(content="Question 2"),
        AIMessage(content="Answer 2"),
    ]
}

Uses last 4 messages for context in next query
```

---

This architecture is:
- **Scalable**: Can handle multiple users with proper deployment
- **Maintainable**: Clear separation of concerns
- **Extensible**: Easy to add new features
- **Robust**: Error handling at each layer
- **Efficient**: Caching and persistence built-in

---

For more details, see DEVELOPMENT.md
