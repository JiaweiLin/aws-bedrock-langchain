# app/streamlit_app.py
import streamlit as st
from app.config import load_config
from app.bedrock_client import BedrockClient
from app.document_chat import DocumentChatManager

# Streamlit UI
def main():
    st.set_page_config(page_title="GenAI App with LangChain & Bedrock", layout="wide")
    
    st.title("🤖 Gen AI App - Built with LangChain and Amazon Bedrock")
    st.markdown("Choose a model from the drop-down box at the right before you begin")
    
    # Initialize the app
    if 'genai_app' not in st.session_state:
        try:
            config = load_config()
            st.session_state.genai_app = BedrockClient(config)
            st.success("✅ Connected to Amazon Bedrock!")
        except Exception as e:
            st.error(f"❌ Failed to connect to Bedrock: {str(e)}")
            st.stop()
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    app_mode = st.sidebar.selectbox(
        "Choose Application Mode",
        ["AI Chat & Generation", "Code Generation", "Document Summary", "Document Chat"]
    )
    
    model_choice = st.sidebar.selectbox(
        "Choose Model",
        ["Claude 3.5 Sonnet V2", "Amazon Titan Text Embeddings V2"]
    )
    
    # Main content area
    if app_mode == "AI Chat & Generation":
        st.header("📚 Educational Content Generator")
        st.markdown("Generate content using conversational AI")
    
        col1, col2 = st.columns(2)
            
        with col1:
            topic = st.text_input("Topic:")
            audience = st.text_input("Target Audience:")
            
        with col2:
            tone = st.selectbox("Tone:", ["professional", "casual", "academic", "friendly"])
            
        if st.button("Generate Educational Content"):
            if topic and audience:
                with st.spinner("Creating educational content..."):
                    content = st.session_state.genai_app.prompt_template_chain(topic, audience, tone)
                    st.write("**Generated Content:**")
                    st.write(content)
    
    elif app_mode == "Code Generation":
        st.header("Code Generator")
        description = st.text_area("Describe what you want to build:", height=100)
        language = st.selectbox("Programming Language:", ["python", "javascript", "java", "cpp", "html", "css"])
        
        if st.button("Generate Code"):
            if description:
                with st.spinner("Generating code..."):
                    code = st.session_state.genai_app.code_generation(description, language)
                    st.write("**Generated Code:**")
                    st.code(code, language=language)
    
    elif app_mode == "Document Summary":
        st.header("Document Summarizer")
        text_input = st.text_area("Paste your document text here:", height=200)
        summary_type = st.selectbox("Summary Type:", ["brief", "detailed", "standard"])
        
        if st.button("Summarize"):
            if text_input:
                with st.spinner("Summarizing document..."):
                    summary = st.session_state.genai_app.document_summarization(text_input, summary_type)
                    st.write("**Summary:**")
                    st.write(summary)
    
    elif app_mode == "Document Chat":
        st.header("📄 Document Chat")
        st.markdown("Upload a document and chat with it using AI!")
        
        # Initialize document chat manager
        if 'doc_chat_manager' not in st.session_state:
            try:
                config = load_config()
                st.session_state.doc_chat_manager = DocumentChatManager(st.session_state.genai_app, config)
            except Exception as e:
                st.error(f"❌ Failed to initialize document chat: {str(e)}")
                st.stop()
        
        # Document upload section
        st.subheader("📤 Upload Document")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=st.session_state.doc_chat_manager.get_supported_formats(),
                help="Supported formats: PDF, DOCX, DOC, TXT"
            )
        
        with col2:
            if st.button("Clear Document") and 'current_doc_name' in st.session_state:
                st.session_state.doc_chat_manager.clear_document()
                if 'current_doc_name' in st.session_state:
                    del st.session_state.current_doc_name
                if 'doc_chat_history' in st.session_state:
                    del st.session_state.doc_chat_history
                st.success("Document cleared!")
                st.rerun()
        
        # Process uploaded file
        if uploaded_file is not None:
            if 'current_doc_name' not in st.session_state or st.session_state.current_doc_name != uploaded_file.name:
                with st.spinner("Processing document..."):
                    try:
                        # Process the uploaded file
                        documents = st.session_state.doc_chat_manager.process_uploaded_file(uploaded_file)
                        
                        # Create vector store
                        num_chunks = st.session_state.doc_chat_manager.create_vectorstore(documents)
                        
                        # Store current document name
                        st.session_state.current_doc_name = uploaded_file.name
                        
                        # Initialize chat history for this document
                        st.session_state.doc_chat_history = []
                        
                        st.success(f"✅ Document processed successfully! Created {num_chunks} text chunks.")
                        
                        # Show document summary
                        with st.expander("📋 Document Summary", expanded=True):
                            summary = st.session_state.doc_chat_manager.get_document_summary()
                            st.write(summary)
                            
                    except Exception as e:
                        st.error(f"❌ Error processing document: {str(e)}")
        
        # Chat interface
        if 'current_doc_name' in st.session_state:
            st.subheader(f"💬 Chat with: {st.session_state.current_doc_name}")
            
            # Initialize chat history if not exists
            if 'doc_chat_history' not in st.session_state:
                st.session_state.doc_chat_history = []
            
            # Display chat history
            if st.session_state.doc_chat_history:
                st.write("**Chat History:**")
                for i, chat in enumerate(st.session_state.doc_chat_history):
                    with st.container():
                        st.write(f"**You:** {chat['question']}")
                        st.write(f"**AI:** {chat['answer']}")
                        
                        # Show sources in an expander
                        if chat.get('sources'):
                            with st.expander(f"📚 Sources for response {i+1}"):
                                for j, source in enumerate(chat['sources']):
                                    st.write(f"**Source {j+1}:**")
                                    st.write(f"*Content:* {source['content']}")
                                    if source['metadata']:
                                        st.write(f"*Metadata:* {source['metadata']}")
                                    st.write("---")
                        st.write("---")
            
            # Chat input
            question = st.text_input("Ask a question about the document:", key="doc_question")
            
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if st.button("Ask", key="ask_doc"):
                    if question:
                        with st.spinner("Searching document and generating response..."):
                            try:
                                response = st.session_state.doc_chat_manager.chat_with_document(question)
                                
                                # Add to chat history
                                st.session_state.doc_chat_history.append(response)
                                
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
            
            with col2:
                if st.button("Clear Chat History", key="clear_doc_chat"):
                    st.session_state.doc_chat_history = []
                    st.session_state.doc_chat_manager.memory.clear()
                    st.success("Chat history cleared!")
                    st.rerun()
        
        else:
            st.info("👆 Please upload a document to start chatting!")

if __name__ == "__main__":
    main()
