import openai
import textwrap
import os
import logging
import datetime
import json
import uuid
from typing import Dict, Any

# Configure logging with function names
logging.basicConfig(
    filename='error_logging.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
)

def load_chat_history() -> Dict[str, Any]:
    """Load chat history from JSON file or create new if not exists."""
    try:
        if os.path.exists('chat_history.json'):
            with open('chat_history.json', 'r') as f:
                return json.load(f)
        return {"interactions": []}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse chat history: {str(e)}")
        return {"interactions": []}
    except Exception as e:
        logging.error(f"Unexpected error loading chat history: {str(e)}")
        return {"interactions": []}

def save_interaction(user_prompt: str, llm_response: str, model: str, processing_time: float) -> None:
    """Save a chat interaction to JSON file."""
    try:
        history = load_chat_history()
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_prompt": user_prompt,
            "llm_response": llm_response,
            "llm_model": model,
            "processing_time": processing_time,
            "session_id": str(uuid.uuid4())
        }
        history["interactions"].append(interaction)
        
        with open('chat_history.json', 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save interaction: {str(e)}")
        print(f"Warning: Failed to save chat history: {str(e)}")

def get_llm_response(prompt: str) -> tuple[str, str, float]:
    """Get response from LLM API and measure processing time."""
    start_time = datetime.datetime.now()
    
    try:
        api_key = os.environ.get('AKASH_API_KEY')
        if not api_key:
            raise ValueError("AKASH_API_KEY environment variable is not set")

        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://chatapi.akash.network/api/v1"
        )

        model = "Meta-Llama-3-1-8B-Instruct-FP8"
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        processing_time = (datetime.datetime.now() - start_time).total_seconds()
        return response.choices[0].message.content, model, processing_time

    except ValueError as ve:
        logging.error(f"Configuration error: {str(ve)}")
        raise
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in LLM response: {str(e)}")
        raise

def main_loop() -> None:
    """Main interaction loop for chat interface."""
    print("Chat interface ready (type 'exit' to quit)")
    
    while True:
        try:
            user_input = input("\nEnter your question: ").strip()
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
                
            if not user_input:
                print("Please enter a question.")
                continue

            response_text, model, proc_time = get_llm_response(user_input)
            print("\nResponse:", textwrap.fill(response_text, 50))
            
            save_interaction(user_input, response_text, model, proc_time)

        except ValueError as ve:
            print(f"Configuration error: {str(ve)}")
            break
        except openai.OpenAIError as e:
            print(f"API Error: {str(e)}")
            continue
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            logging.error(f"Main loop error: {str(e)}")
            continue

if __name__ == "__main__":
    try:
        main_loop()
    except Exception as e:
        logging.error(f"Fatal error in main: {str(e)}")
        print(f"Fatal error occurred: {str(e)}")
