"""Main Streamlit application for Chat with Your Notes RAG app."""
import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag_chain import RAGChain

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Chat with Your Notes",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    /* Main styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
    }
    
    /* Header styling */
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1.2rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Source citation styling */
    .source-citation {
        font-size: 0.85rem;
        color: #555;
        font-style: italic;
        margin-top: 0.75rem;
        padding: 0.75rem;
        background-color: #f9f9f9;
        border-left: 4px solid #667eea;
        border-radius: 0.4rem;
    }
    
    /* Upload section styling */
    .upload-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        border: 2px dashed #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    
    .stError {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    
    .stInfo {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
    }
    
    /* File info styling */
    .file-info {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.divider()
    
    # Connection status
    st.subheader("🔌 Ollama Connection")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            st.success("✅ Ollama is running (FREE local AI)")
            st.session_state.api_key_valid = True
            if st.session_state.rag_chain is None:
                st.session_state.rag_chain = RAGChain()
                if st.session_state.rag_chain.load_existing_store():
                    st.info("ℹ️ Existing documents loaded!")
        else:
            st.error("❌ Ollama connection failed")
            st.session_state.api_key_valid = False
    except:
        st.error("❌ Ollama not running. Please start it:")
        st.code("ollama serve", language="bash")
        st.session_state.api_key_valid = False
    
    st.divider()
    
    # Document Upload Section
    if st.session_state.api_key_valid:
        st.subheader("📤 Upload Documents")
        st.markdown(
            '<div class="upload-section">',
            unsafe_allow_html=True
        )
        
        uploaded_files = st.file_uploader(
            "Upload document files",
            type=["pdf", "docx", "pptx"],
            accept_multiple_files=True,
            key="file_uploader",
            help="Upload PDF, Word documents, or PowerPoint presentations"
        )
        
        if uploaded_files:
            with st.spinner("📖 Processing documents..."):
                for uploaded_file in uploaded_files:
                    # Only process if not already processed
                    if uploaded_file.name not in st.session_state.uploaded_files:
                        # Save temporary file
                        temp_path = f"./uploads/{uploaded_file.name}"
                        os.makedirs("./uploads", exist_ok=True)
                        
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        try:
                            # Process document (PDF, DOCX, or PPTX)
                            from app.pdf_processor import process_document_file
                            chunked_docs, file_name, file_type = process_document_file(temp_path)
                            
                            # Add to RAG chain
                            result_msg = st.session_state.rag_chain.add_documents(
                                chunked_docs, 
                                file_name
                            )
                            
                            # Track uploaded file
                            st.session_state.uploaded_files[uploaded_file.name] = {
                                "size": len(chunked_docs),
                                "chunks": len(chunked_docs),
                                "type": file_type
                            }
                            
                            st.success(f"✅ {file_name} ({file_type}) loaded successfully!")
                            
                        except Exception as e:
                            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show loaded documents
        if st.session_state.uploaded_files:
            st.subheader("📚 Loaded Documents")
            cols = st.columns(min(3, len(st.session_state.uploaded_files)))
            for idx, (file_name, info) in enumerate(st.session_state.uploaded_files.items()):
                with cols[idx % len(cols)]:
                    file_type = info.get("type", "PDF")
                    icon_map = {"PDF": "📄", "WORD": "📘", "POWERPOINT": "📊"}
                    icon = icon_map.get(file_type, "📄")
                    
                    st.markdown(f"""
                        <div class="file-info">
                            <strong>{icon} {file_name}</strong><br>
                            <small>Type: {file_type}</small><br>
                            <small>Chunks: {info.get('chunks', 0)}</small>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.divider()
        
        # Model Settings
        st.subheader("🎛️ Model Settings")
        
        temperature = st.slider(
            "Temperature (Creativity vs Precision)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Lower = more precise, Higher = more creative"
        )
        
        if st.session_state.rag_chain:
            st.session_state.rag_chain.set_temperature(temperature)
        
        st.divider()
        
        # Chat Controls
        st.subheader("💬 Chat Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.chat_history = []
                if st.session_state.rag_chain:
                    st.session_state.rag_chain.clear_memory()
                st.success("Chat history cleared!")
                st.rerun()
        
        with col2:
            if st.button("📊 Collection Info", use_container_width=True):
                if st.session_state.rag_chain:
                    info = st.session_state.rag_chain.get_collection_info()
                    st.info(f"Total chunks: {info.get('total_chunks', 0)}")
    else:
        st.warning("⚠️ Please enter a valid OpenAI API key to proceed")

# Main Chat Interface
st.markdown("""
    <div class="header-section">
        <h1>📚 Chat with Your Notes</h1>
        <p>Free AI powered by Ollama - Ask questions about your documents (no API fees!)</p>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.api_key_valid:
    st.error("⚠️ **Ollama is not running!**")
    st.info("""
    1. Download Ollama from https://ollama.ai
    2. Install it and open a terminal
    3. Run: `ollama serve`
    4. Keep it running in the background
    5. Then refresh this page
    """)
elif not st.session_state.uploaded_files:
    st.info("👈 Upload documents in the sidebar to start asking questions")
else:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("📖 Sources"):
                    for source in message["sources"]:
                        st.markdown(
                            f"""<div class="source-citation">
                            <strong>📄 {source['file']}</strong> - Page {source['page']}
                            </div>""",
                            unsafe_allow_html=True
                        )
    
    # Chat input
    user_input = st.chat_input(
        "Ask a question about your notes...",
        placeholder="e.g., 'Summarize chapter 3' or 'Explain photosynthesis'"
    )
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = st.session_state.rag_chain.query(user_input)
                answer = response["answer"]
                sources = response["sources"]
            
            # Display answer
            st.markdown(answer)
            
            # Display sources if available
            if sources:
                with st.expander("📖 Sources Used"):
                    for source in sources:
                        st.markdown(
                            f"""<div class="source-citation">
                            <strong>📄 {source['file']}</strong> - Page {source['page']}
                            </div>""",
                            unsafe_allow_html=True
                        )
            else:
                st.caption("⚠️ No sources found for this answer")
        
        # Add assistant message to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })

# Footer
st.divider()
st.caption("""
    **Chat with Your Notes** - A RAG (Retrieval-Augmented Generation) application
    Built with Streamlit, LangChain, ChromaDB, and OpenAI
""")
