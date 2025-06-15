# app/aws_client.py
import boto3
from langchain_aws import BedrockLLM, ChatBedrock

def create_bedrock_client(config):
    """Setup different Bedrock models for various use cases"""
    
    # Claude 4 Sonnet for conversational AI
    claude_llm = ChatBedrock(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        client=initialize_bedrock(config),
        model_kwargs={
            "max_tokens": 4096,
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    
    # Titan for text generation
    titan_llm = BedrockLLM(
        model_id="amazon.titan-embed-text-v2:0",
        client=initialize_bedrock(config),
        model_kwargs={
            "maxTokenCount": 4096,
            "temperature": 0.7,
            "topP": 0.9
        }
    )
    
    return claude_llm, titan_llm

def initialize_bedrock(config):
    """Initialize Bedrock client with proper configuration"""
    bedrock_client = boto3.client(
        service_name=config["aws_service_name"],
        region_name=config["aws_region_name"],
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"]
    )
    return bedrock_client
