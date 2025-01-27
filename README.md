# Akash Network Chat API Client

A Python client for interacting with the Akash Network Chat API, available in both CLI and Streamlit interface versions.

# Repository
https://github.com/pleabargain/akash-chat-test

## Setup

1. Ensure you have Python 3.x installed
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variable (Optional - can also be entered in Streamlit UI):
```bash
# On Windows
set AKASH_API_KEY=your_api_key_here

# On Linux/Mac
export AKASH_API_KEY=your_api_key_here
```

## Usage

### CLI Version (main.py)
Run the command-line interface version:
```bash
python main.py
```

The CLI version provides:
- Interactive command-line chat interface
- Error logging to error_logging.log
- Chat history saved to chat_history.json
- Environment variable based API key configuration

### Streamlit Version (streamlit_app.py)
Run the Streamlit web interface version:
```bash
streamlit run streamlit_app.py
```

The Streamlit version provides:
- Web-based user interface
- API key input if not found in environment
- Four main tabs:
  1. README: Documentation view
  2. Source Code: View the original CLI implementation
  3. Errors: View error logs
  4. JSON History: View chat history
- Persistent chat input at the top of the interface
- Session-based API key storage
- Real-time chat history updates

## Features

- Integration with Akash Network Chat API
- Support for Meta-Llama-3-1-8B-Instruct-FP8 model
- Error logging and handling
- Chat history persistence
- Secure API key management

## API Documentation

For complete API documentation, visit:
[Akash Network Chat API Documentation](https://chatapi.akash.network/)

## Security

- Never hardcode your API key in the source code
- Always use environment variables or the secure input field in Streamlit for sensitive credentials
- Keep your API key secure and do not share it
- The Streamlit version stores the API key in session state, which is cleared when the browser is closed

## Branches

- main: Contains the original CLI implementation
- streamlit-ui: Contains both CLI and Streamlit implementations
