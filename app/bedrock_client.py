# app/bedrock_client_deepseek.py
from app.aws_client import create_bedrock_client
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

class BedrockClient:
    """Client for interacting with AWS Bedrock using the Deepseek-R1 model."""
    
    def __init__(self, config):
        """Initialize the Bedrock client with configuration."""
        # Use the universal boto3 client for AWS Bedrock
        self.claude_llm, self.titan_llm  = create_bedrock_client(config)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    def prompt_template_chain(self, topic, audience, tone="professional"):
        """Use prompt templates for structured generation"""
        template = """
        Create a comprehensive explanation about {topic} for {audience}.
        Use a {tone} tone and include:
        1. A clear introduction
        2. Key concepts explained simply
        3. Practical examples
        4. A conclusion with key takeaways
        
        Topic: {topic}
        Audience: {audience}
        Tone: {tone}
        """
        
        prompt = PromptTemplate(
            input_variables=["topic", "audience", "tone"],
            template=template
        )
        
        chain = LLMChain(
            llm=self.claude_llm,
            prompt=prompt,
            verbose=True
        )
        
        return chain.run(topic=topic, audience=audience, tone=tone)
    
    def conversational_chain(self, user_input):
        """Conversational AI with memory"""
        template = """
        You are a knowledgeable AI assistant. Use the conversation history to provide contextual responses.
        
        Chat History: {chat_history}
        Human: {user_input}
        AI Assistant:
        """
        
        prompt = PromptTemplate(
            input_variables=["chat_history", "user_input"],
            template=template
        )
        
        chain = LLMChain(
            llm=self.claude_llm,
            prompt=prompt,
            memory=self.memory,
            verbose=True
        )
        
        response = chain.run(user_input=user_input)
        return response
    
    def code_generation(self, description, language="python"):
        """Generate code based on description"""
        template = """
        Generate clean, well-documented {language} code for the following requirement:
        {description}
        
        Include:
        - Proper comments
        - Error handling where appropriate
        - Best practices
        - Example usage if applicable
        
        Requirement: {description}
        Programming Language: {language}
        """
        
        prompt = PromptTemplate(
            input_variables=["description", "language"],
            template=template
        )
        
        chain = LLMChain(
            llm=self.claude_llm,
            prompt=prompt
        )
        
        return chain.run(description=description, language=language)
    
    def document_summarization(self, text, summary_type="brief"):
        """Summarize documents"""
        if summary_type == "brief":
            template = "Provide a brief summary of the following text in 2-3 sentences:\n\n{text}"
        elif summary_type == "detailed":
            template = """
            Provide a detailed summary of the following text including:
            - Main points
            - Key findings or conclusions
            - Important details
            
            Text: {text}
            """
        else:
            template = "Summarize the following text:\n\n{text}"
        
        prompt = PromptTemplate(
            input_variables=["text"],
            template=template
        )
        
        chain = LLMChain(
            llm=self.claude_llm,
            prompt=prompt
        )
        
        return chain.run(text=text)