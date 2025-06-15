# app/main.py
from app.config import load_config
from app.bedrock_client import BedrockClientDeepseek

def main():
    """Main function to run the Deepseek streaming application."""
    try:
        # Load configuration and initialize Deepseek client
        config = load_config()
        client = BedrockClientDeepseek(config)
        
        # Define the user query and custom system prompt
        system_message = "You're a helpful assistant that specializes in physics."
        user_message = "What is the speed of light?"
        
        # Create conversation structure with the system prompt
        conversation = client.create_conversation(user_message, system_message)
        
        ### Inferencing without streaming ### -> Uncomment this block to use non-streaming
        # Query the model (non-streaming version)
        # response = client.query_model(conversation)
        
        # Print both the reasoning and final response
        # print("Reasoning:")
        # print(response["reasoning_text"])
        # print("\nFinal Response:")
        # print(response["response_text"])
        
        
        ## Inferencing with streaming
        # Flags to track whether headers have been printed for streaming
        printed_reasoning, printed_final = False, False
        
        # Process streaming tokens in real time
        for token in client.stream_query_model(conversation):
            if token["part"] == "reasoning":
                if not printed_reasoning:
                    print("\nReasoning:\n", end="")
                    printed_reasoning = True
                print(token["text"], end="", flush=True)
            
            elif token["part"] == "final":
                if not printed_final:
                    print("\nFinal Response:", end="")
                    printed_final = True
                print(token["text"], end="", flush=True)
    
    except Exception as e:
        print(str(e))
        exit(1)

if __name__ == "__main__":
    main()
