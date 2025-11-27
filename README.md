# Chat with Your Notes - RAG Application

A powerful Retrieval-Augmented Generation (RAG) application that lets you upload PDF textbooks or class notes and ask questions about them. Instead of searching the web, you have a personalized AI that knows only your documents.

## ✨ Features

### Core RAG Capabilities
- **📚 Multi-PDF Support**: Upload 3-4 PDFs (textbooks, lecture notes, etc.)
- **🔍 Smart Retrieval**: Uses ChromaDB vector database for semantic search
- **📖 Source Citations**: Every answer includes page numbers and file names
- **💾 Memory & Context**: Maintains conversation history for follow-up questions
- **🎨 Beautiful UI**: Clean, intuitive Streamlit interface

### Advanced Features
- **⏳ Progress Indicator**: Visual feedback while processing PDFs
- **🎚️ Temperature Slider**: Control creativity vs. precision of responses (0-1)
- **🗑️ Clear Chat Button**: Reset conversation without reloading
- **📊 Collection Info**: View statistics about loaded documents
- **🔐 Secure API Input**: Password-protected OpenAI API key field

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend UI** | Streamlit 1.28.1 |
| **LLM Framework** | LangChain 0.1.0 |
| **Vector Database** | ChromaDB 0.4.11 |
| **Language Model** | GPT-3.5-Turbo (OpenAI) |
| **Embeddings** | OpenAI Embeddings |
| **PDF Processing** | PyPDF 3.17.1 |
| **Config Management** | python-dotenv |

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ~500MB disk space for ChromaDB vector store

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Navigate to project directory
cd rag-notes-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...your-key-here...
```

Alternatively, you can enter the API key directly in the app's sidebar.

### 3. Run the Application
```bash
streamlit run app/app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Uploading Documents
1. Enter your OpenAI API key in the sidebar
2. Click the "Upload PDF files" button
3. Select 1-4 PDF files
4. Wait for the "Reading PDF..." processing indicator
5. See confirmation messages with page and chunk counts

### Asking Questions
1. Type your question in the chat input box
2. Examples:
   - "Summarize chapter 3"
   - "Explain the concept of photosynthesis"
   - "What are the main points about mitochondria?"
   - "Can you explain that further?" (follow-up questions work too!)

### Adjusting Settings
- **Temperature Slider**: Lower (0.3) for precise, factual answers; Higher (0.8) for creative responses
- **Clear Chat**: Removes conversation history but keeps documents loaded
- **Collection Info**: Shows total chunks indexed from all PDFs

## 🏗️ Project Structure

```
rag-notes-app/
├── app/
│   ├── __init__.py
│   ├── app.py                 # Main Streamlit application
│   ├── pdf_processor.py       # PDF loading and chunking
│   └── rag_chain.py          # RAG chain with memory
├── uploads/                   # Temporary PDF storage
├── requirements.txt           # Python dependencies
├── .env.example              # Example environment file
├── .gitignore
└── README.md
```

## 🔧 How It Works

### 1. Document Processing
- PDFs are loaded using PyPDF2
- Each page is extracted as metadata for citations
- Text is split into overlapping chunks (1000 chars, 200 char overlap)
- Smart chunking preserves context

### 2. Embedding & Storage
- ChromaDB generates embeddings using OpenAI's embedding model
- Embeddings are stored in a persistent vector database
- Supports incremental addition of documents

### 3. Retrieval & Generation (RAG)
- User query is embedded using the same embedding model
- Top 4 most relevant chunks are retrieved from the vector database
- Context + query is sent to GPT-3.5-Turbo with conversation history
- Model generates answer with source citations

### 4. Chat Memory
- Last 4 messages are preserved in the prompt
- Allows coherent follow-up questions
- Memory can be cleared independently

## 📊 Example Queries

### Academic
```
"Summarize the photosynthesis chapter"
"What are the steps of cellular respiration?"
"Compare mitochondria and chloroplasts"
```

### Follow-ups
```
"Can you explain that more simply?"
"Give me an example"
"What's the significance of this?"
```

### Multiple Files
```
"Compare chapter 1 and chapter 2"
"How does this relate to what was in the lecture notes?"
```

## ⚙️ Configuration

### Chunk Settings (in `pdf_processor.py`)
```python
chunk_size = 1000          # Characters per chunk
chunk_overlap = 200        # Overlap between chunks
```

### Retrieval Settings (in `rag_chain.py`)
```python
retriever search_kwargs = {"k": 4}  # Number of chunks to retrieve
```

### Model Settings (in Streamlit UI)
- **Temperature**: 0.0 - 1.0 (controlled via slider)
- **Model**: GPT-3.5-Turbo (can be changed to GPT-4)

## 🐛 Troubleshooting

### "Invalid API Key" Error
- Check that your OpenAI API key is correct
- Ensure the key has API access enabled
- Check for spaces or typos

### PDFs Not Processing
- Ensure PDFs have text (not scanned images)
- Check that PDFs aren't corrupted
- Try re-uploading the file

### Slow Responses
- First query after upload is slower (ChromaDB initialization)
- Subsequent queries should be fast
- Temperature affects response time (higher = slower)

### "No sources found"
- Means retrieval didn't find relevant chunks
- Try asking more specific questions
- Check that PDFs contain relevant content

## 🔒 Security & Privacy

- API key is only used for OpenAI API calls
- PDFs are processed locally
- ChromaDB vector store is stored locally (`.chroma/` directory)
- No data is sent to external servers except OpenAI

## 💰 Cost Considerations

Costs are based on OpenAI API usage:
- **Embedding Generation**: ~$0.0001 per 1K tokens
- **Chat Completion**: GPT-3.5-Turbo (~$0.0005-0.002 per 1K tokens)
- **Estimate**: ~$0.01 per conversation turn (varies by document size)

## 🚀 Future Enhancements

- [ ] Support for additional file types (DOCX, TXT, PPTX)
- [ ] Local LLM support (Ollama, LLaMA)
- [ ] Advanced search filters
- [ ] Document highlighting in chat
- [ ] Export conversation history
- [ ] Multi-language support
- [ ] User authentication & document sharing
- [ ] Cost tracking dashboard

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review LangChain documentation: https://python.langchain.com/
3. Check ChromaDB docs: https://docs.trychroma.com/

## 📚 Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [RAG Explained](https://docs.anthropic.com/claude/docs/retrieval-augmented-generation)

---

**Built with ❤️ using Streamlit, LangChain, and ChromaDB**
