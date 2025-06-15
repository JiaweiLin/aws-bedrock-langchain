# app/research_agent.py
import streamlit as st
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.tools import BaseTool
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.schema import AgentAction, AgentFinish
from typing import Optional, Type, Any, List, Dict
import requests
import json
import re
import os
from datetime import datetime
import math

class CalculatorTool(BaseTool):
    """A simple calculator tool for mathematical operations."""
    name: str = "calculator"
    description: str = "Useful for performing mathematical calculations. Input should be a mathematical expression like '2+2' or 'sqrt(16)' or '10*5/2'"
    
    def _run(self, query: str) -> str:
        """Execute the calculator tool."""
        try:
            # Clean the query
            query = query.strip()
            
            # Replace common mathematical functions
            query = query.replace('sqrt', 'math.sqrt')
            query = query.replace('sin', 'math.sin')
            query = query.replace('cos', 'math.cos')
            query = query.replace('tan', 'math.tan')
            query = query.replace('log', 'math.log')
            query = query.replace('pi', 'math.pi')
            query = query.replace('e', 'math.e')
            query = query.replace('^', '**')  # Replace ^ with ** for power
            
            # Evaluate the expression safely
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round, "min": min, "max": max})
            
            result = eval(query, {"__builtins__": {}}, allowed_names)
            return f"The result of {query} is: {result}"
        except Exception as e:
            return f"Error in calculation: {str(e)}. Please check your mathematical expression."
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool."""
        return self._run(query)

class TextAnalyzerTool(BaseTool):
    """A tool for analyzing text content."""
    name: str = "text_analyzer"
    description: str = "Useful for analyzing text content. Can count words, characters, sentences, find keywords, and provide basic text statistics. Input should be the text to analyze."
    
    def _run(self, text: str) -> str:
        """Execute the text analyzer tool."""
        try:
            # Basic text statistics
            word_count = len(text.split())
            char_count = len(text)
            char_count_no_spaces = len(text.replace(' ', ''))
            sentence_count = len(re.findall(r'[.!?]+', text))
            paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
            
            # Find most common words (simple approach)
            words = re.findall(r'\b\w+\b', text.lower())
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Only count words longer than 3 characters
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top 5 most common words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Calculate reading time (average 200 words per minute)
            reading_time = math.ceil(word_count / 200)
            
            analysis = f"""
Text Analysis Results:
- Word count: {word_count}
- Character count: {char_count}
- Character count (no spaces): {char_count_no_spaces}
- Sentence count: {sentence_count}
- Paragraph count: {paragraph_count}
- Estimated reading time: {reading_time} minute(s)

Top 5 most frequent words:
"""
            for word, freq in top_words:
                analysis += f"- {word}: {freq} times\n"
            
            return analysis
        except Exception as e:
            return f"Error analyzing text: {str(e)}"
    
    async def _arun(self, text: str) -> str:
        """Async version of the tool."""
        return self._run(text)

class DateTimeTool(BaseTool):
    """A tool for date and time operations."""
    name: str = "datetime_tool"
    description: str = "Useful for getting current date/time, calculating date differences, or formatting dates. Input can be 'current' for current datetime, or date calculations like 'days between 2024-01-01 and 2024-12-31'"
    
    def _run(self, query: str) -> str:
        """Execute the datetime tool."""
        try:
            query = query.lower().strip()
            
            if query == "current" or query == "now":
                current_time = datetime.now()
                return f"Current date and time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            elif "days between" in query:
                # Extract dates from query
                dates = re.findall(r'\d{4}-\d{2}-\d{2}', query)
                if len(dates) >= 2:
                    date1 = datetime.strptime(dates[0], '%Y-%m-%d')
                    date2 = datetime.strptime(dates[1], '%Y-%m-%d')
                    diff = abs((date2 - date1).days)
                    return f"Days between {dates[0]} and {dates[1]}: {diff} days"
                else:
                    return "Please provide dates in YYYY-MM-DD format"
            
            else:
                return "Available operations: 'current' for current datetime, 'days between YYYY-MM-DD and YYYY-MM-DD' for date calculations"
        
        except Exception as e:
            return f"Error with date/time operation: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool."""
        return self._run(query)

class ResearchAgent:
    """A research assistant agent that uses multiple tools to help with research tasks."""
    
    def __init__(self, llm):
        """Initialize the research agent with tools and memory."""
        self.llm = llm
        
        # Initialize tools
        self.tools = [
            CalculatorTool(),
            TextAnalyzerTool(),
            DateTimeTool()
        ]
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate"
        )
    
    def research(self, query: str) -> Dict[str, Any]:
        """Conduct research using the agent and tools."""
        try:
            # Run the agent
            response = self.agent.run(query)
            
            return {
                "success": True,
                "response": response,
                "tools_used": [tool.name for tool in self.tools],
                "error": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "response": f"I encountered an error while researching: {str(e)}",
                "tools_used": [],
                "error": str(e)
            }
    
    def get_available_tools(self) -> List[Dict[str, str]]:
        """Get information about available tools."""
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools
        ]
    
    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()
