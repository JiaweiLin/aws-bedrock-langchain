__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# app/document_chat.py
import os
import tempfile
from typing import List, Dict, Any
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_aws import BedrockEmbeddings
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document

class DocumentChatManager:
    """Manages document upload, processing, and chat functionality using RAG."""
    
    def __init__(self, bedrock_client, config):
        """Initialize the document chat manager."""
        self.bedrock_client = bedrock_client
        self.config = config
        self.claude_llm = bedrock_client.claude_llm
        
        # Initialize embeddings using Bedrock
        self.embeddings = BedrockEmbeddings(
            client=bedrock_client.claude_llm.client,
            model_id="amazon.titan-embed-text-v2:0"
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Initialize memory for conversation
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="result"
        )
        
        self.vectorstore = None
        self.qa_chain = None
        self.current_document = None
    
    def process_uploaded_file(self, uploaded_file) -> List[Document]:
        """Process uploaded file and extract text content."""
        documents = []
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                documents = self._process_pdf(tmp_file_path)
            elif file_extension in ['docx', 'doc']:
                documents = self._process_docx(tmp_file_path)
            elif file_extension == 'txt':
                documents = self._process_txt(tmp_file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            # Add metadata to documents
            for doc in documents:
                doc.metadata.update({
                    "source": uploaded_file.name,
                    "file_type": file_extension
                })
            
            return documents
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
    
    def _process_pdf(self, file_path: str) -> List[Document]:
        """Process PDF file and extract text."""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    
    def _process_docx(self, file_path: str) -> List[Document]:
        """Process DOCX file and extract text."""
        loader = Docx2txtLoader(file_path)
        documents = loader.load()
        return documents
    
    def _process_txt(self, file_path: str) -> List[Document]:
        """Process TXT file and extract text."""
        loader = TextLoader(file_path)
        documents = loader.load()
        return documents
    
    def create_vectorstore(self, documents: List[Document]):
        """Create vector store from documents."""
        # Split documents into chunks
        texts = self.text_splitter.split_documents(documents)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=None  # In-memory storage
        )
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.claude_llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            ),
            memory=self.memory,
            return_source_documents=True
        )
        
        return len(texts)
    
    def chat_with_document(self, question: str) -> Dict[str, Any]:
        """Chat with the uploaded document using RAG."""
        if not self.qa_chain:
            raise ValueError("No document has been processed. Please upload a document first.")
        
        try:
            # Get response from QA chain
            response = self.qa_chain({"query": question})
            
            # Extract source documents
            source_docs = response.get("source_documents", [])
            sources = []
            for doc in source_docs:
                sources.append({
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                })
            
            return {
                "answer": response["result"],
                "sources": sources,
                "question": question
            }
            
        except Exception as e:
            raise Exception(f"Error during document chat: {str(e)}")
    
    def get_document_summary(self) -> str:
        """Get a summary of the uploaded document."""
        if not self.vectorstore:
            return "No document uploaded."
        
        # Get a few chunks from the document
        docs = self.vectorstore.similarity_search("summary overview content", k=3)
        combined_text = "\n\n".join([doc.page_content for doc in docs])
        
        # Generate summary
        summary_prompt = f"""
        Please provide a concise summary of the following document content:
        
        {combined_text}
        
        Summary:
        """
        
        try:
            response = self.claude_llm.invoke([{"role": "user", "content": summary_prompt}])
            return response.content
        except:
            return "Unable to generate summary at this time."
    
    def clear_document(self):
        """Clear the current document and reset the chat."""
        self.vectorstore = None
        self.qa_chain = None
        self.current_document = None
        self.memory.clear()
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        return ["pdf", "docx", "doc", "txt"]
