# AWS Bedrock LangChain Integration

A comprehensive Python-based generative AI application that integrates AWS Bedrock with LangChain to provide multiple AI-powered functionalities, including a new **Research Assistant** feature using LangChain agents and tools.

## 🚀 Features

### Core AI Capabilities
- **Educational Content Creator** - Generate structured educational content with customizable tone and audience
- **Code Generation** - Multi-language code generation with best practices
- **Document Summarization** - Brief, detailed, or standard document summaries
- **Document Chat with RAG** - Upload and chat with documents using retrieval-augmented generation
- **🆕 Research Assistant** - AI agent with multiple tools for research, calculations, and analysis

### Research Assistant Tools
The new Research Assistant uses LangChain agents with the following tools:
- **Calculator Tool** - Mathematical calculations (basic math, trigonometry, logarithms)
- **Text Analyzer Tool** - Text statistics, word count, reading time, keyword analysis
- **DateTime Tool** - Current date/time, date calculations, time differences

## 🏗️ Architecture

### Multi-Model Support
- **Claude 3.5 Sonnet V2** (`us.anthropic.claude-3-5-sonnet-20241022-v2:0`) - Primary conversational AI
- **Amazon Titan** (`amazon.titan-embed-text-v2:0`) - Text generation and embeddings

### Multiple Interfaces
- **Web Interface** (`streamlit_app.py`) - Interactive Streamlit application
- **CLI Interface** (`main.py`) - Command-line interaction
- **Research Agent CLI** (`research_agent_cli.py`) - Test script for the Research Assistant

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aws-bedrock-langchain
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials**
   - Set up AWS credentials with Bedrock access
   - Configure Streamlit secrets or environment variables

## 🔧 Configuration

### AWS Setup
1. Create an IAM user with Bedrock permissions
2. Ensure model access for Claude 3 Sonnet V2 and Amazon Titan
3. Configure credentials in `.streamlit/secrets.toml`:
   ```toml
   AWS_ACCESS_KEY_ID = "your_access_key"
   AWS_SECRET_ACCESS_KEY = "your_secret_key"
   ```

### Environment Variables (Alternative)
```bash
export AWS_SERVICE_NAME=bedrock-runtime
export AWS_REGION_NAME=us-east-1
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

## 🚀 Usage

### Web Application
```bash
streamlit run streamlit_app.py
```

### CLI Interface
```bash
python main.py
```

### Research Assistant CLI Test
```bash
python research_agent_cli.py
```

## 🔬 Research Assistant Examples

The Research Assistant can handle various types of queries:

### Mathematical Calculations
```
Query: "Calculate the square root of 144"
Response: Uses Calculator Tool → "The result of sqrt(144) is: 12.0"
```

### Text Analysis
```
Query: "Analyze this text: LangChain is a framework..."
Response: Uses Text Analyzer Tool → Provides word count, reading time, statistics
```

### Date/Time Operations
```
Query: "What is the current date and time?"
Response: Uses DateTime Tool → "Current date and time: 2024-06-15 22:24:00"
```

## 📁 Project Structure

```
aws-bedrock-langchain/
├── app/
│   ├── __init__.py
│   ├── aws_client.py          # AWS Bedrock client setup
│   ├── bedrock_client.py      # Main AI functionalities
│   ├── config.py              # Configuration management
│   ├── document_chat.py       # RAG functionality
│   └── research_agent.py      # 🆕 LangChain agents and tools
├── main.py                    # CLI entry point
├── streamlit_app.py           # Web UI with Research Assistant
├── document_chat_cli.py       # Document chat test script
├── research_agent_cli.py      # 🆕 Research Assistant test script
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🛠️ Technical Details

### LangChain Agents Implementation
The Research Assistant uses:
- **Agent Type**: `CONVERSATIONAL_REACT_DESCRIPTION`
- **Memory**: `ConversationBufferMemory` for context retention
- **Tools**: Custom BaseTool implementations
- **LLM**: Claude 3 Sonnet V2 for reasoning and tool selection

### Custom Tools
Each tool inherits from `langchain.tools.BaseTool` and implements:
- `_run()` method for synchronous execution
- `_arun()` method for asynchronous execution
- Proper error handling and validation

## 🔍 Dependencies

### Core Dependencies
- `boto3` - AWS SDK
- `langchain` - LLM application framework
- `langchain-aws` - AWS integrations
- `streamlit` - Web interface

### Document Processing
- `pypdf2` - PDF processing
- `python-docx` - DOCX processing
- `faiss-cpu` - Vector similarity search
- `chromadb` - Vector database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Related Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [LangChain Documentation](https://python.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Note**: This project serves as a starter template for building AI applications with AWS Bedrock and LangChain, featuring advanced agent-based interactions and multiple AI capabilities.
