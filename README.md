# Akash Network Chat API Client

A Python client for interacting with the Akash Network Chat API.

## Setup

1. Ensure you have Python 3.x installed
2. Install required dependencies:
```bash
pip install openai
```

3. Set up your environment variable:
```bash
# On Windows
set AKASH_API_KEY=your_api_key_here

# On Linux/Mac
export AKASH_API_KEY=your_api_key_here
```

## Usage

```python
import openai
import os

client = openai.OpenAI(
    akash_api_key=os.environ['AKASH_API_KEY'],
    base_url="https://chatapi.akash.network/api/v1"
)

response = client.chat.completions.create(
    model="Meta-Llama-3-1-8B-Instruct-FP8",
    messages=[{"role": "user", "content": "Your message here"}]
)
```

## API Documentation

For complete API documentation, visit:
[Akash Network Chat API Documentation](https://chatapi.akash.network/)

## Security

- Never hardcode your API key in the source code
- Always use environment variables for sensitive credentials
- Keep your API key secure and do not share it
