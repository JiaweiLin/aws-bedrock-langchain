#!/usr/bin/env python3
"""
CLI test script for the Research Agent feature.
This script demonstrates the LangChain agents and tools functionality.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import load_config
from app.bedrock_client import BedrockClient
from app.research_agent import ResearchAgent

def main():
    """Main function to test the Research Agent."""
    print("🔬 Research Agent CLI Test")
    print("=" * 50)
    
    try:
        # Initialize the Bedrock client
        print("Initializing AWS Bedrock client...")
        config = load_config()
        bedrock_client = BedrockClient(config)
        print("✅ Bedrock client initialized successfully!")
        
        # Initialize the Research Agent
        print("Initializing Research Agent...")
        research_agent = ResearchAgent(bedrock_client.claude_llm)
        print("✅ Research Agent initialized successfully!")
        
        # Show available tools
        print("\n🛠️ Available Tools:")
        tools = research_agent.get_available_tools()
        for i, tool in enumerate(tools, 1):
            print(f"{i}. {tool['name']}: {tool['description']}")
        
        print("\n" + "=" * 50)
        print("Testing Research Agent with sample queries...")
        print("=" * 50)
        
        # Test queries
        test_queries = [
            "Calculate the square root of 144",
            "What is the current date and time?",
            "Tell me about Python programming language",
            "Analyze this text: LangChain is a framework for developing applications powered by language models. It provides tools for chaining together different components.",
            "How many days are there between 2024-01-01 and 2024-12-31?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test Query {i}: {query}")
            print("-" * 40)
            
            try:
                result = research_agent.research(query)
                
                if result['success']:
                    print(f"✅ Response: {result['response']}")
                    if result['tools_used']:
                        print(f"🔧 Tools available: {', '.join(result['tools_used'])}")
                else:
                    print(f"❌ Error: {result['response']}")
                    if result['error']:
                        print(f"Details: {result['error']}")
                        
            except Exception as e:
                print(f"❌ Exception occurred: {str(e)}")
            
            print("-" * 40)
        
        print("\n" + "=" * 50)
        print("🎉 Research Agent testing completed!")
        print("You can now run the Streamlit app to use the Research Assistant interactively.")
        print("Command: streamlit run streamlit_app.py")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Failed to initialize: {str(e)}")
        print("Make sure your AWS credentials are properly configured.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
