#!/usr/bin/env python3
"""
CLI script to test document chat functionality
"""

import os
import sys
from app.config import load_config
from app.bedrock_client import BedrockClient
from app.document_chat import DocumentChatManager

def main():
    """Main function to test document chat via CLI."""
    print("🤖 Document Chat CLI Test")
    print("=" * 50)
    
    try:
        # Load configuration
        print("Loading configuration...")
        config = load_config()
        
        # Initialize Bedrock client
        print("Initializing Bedrock client...")
        bedrock_client = BedrockClient(config)
        
        # Initialize document chat manager
        print("Initializing document chat manager...")
        doc_chat = DocumentChatManager(bedrock_client, config)
        
        print("✅ All components initialized successfully!")
        print("\nSupported file formats:", ", ".join(doc_chat.get_supported_formats()))
        
        # Simple test
        print("\n📄 Document Chat functionality is ready!")
        print("Use the Streamlit web interface to upload documents and chat with them.")
        print("Run: streamlit run streamlit_app.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
