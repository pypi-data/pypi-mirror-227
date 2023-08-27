# api_calls.py

This script is part of a larger module named 'abstract_ai'. It encapsulates a collection of functions and utilities that facilitate seamless interaction with OpenAI's GPT-3 language model.

## Synopsis

The script primarily serves as an interface to interact with OpenAI GPT-3 model. The core functionality of the script revolves around making POST requests and managing JSON responses from the OpenAI API server.

### Functions
- `get_openai_key`: Retrieves the OpenAI API key from the environment variables.
- `load_openai_key`: Loads the OpenAI API key for authentication.
- `headers`: Returns the headers for the API request.
- `post_request`: Sends POST requests to the API server and handles the response it receives.
- `hard_request`, `quick_request`: These functions send different types of requests to the OpenAI API.
- `default_instructions`, `create_chunk_communication`: These functions are responsible for generating instructions and communications for data chunk handling.
- `safe_send`: This function sends data chunks safely and handles any exceptions throughout the process.

## Prerequisites

An environment variable named 'OPENAI_API_KEY' needs to be set prior to execution of this script with your OpenAI API key.

## Author
Alex Putkoff  (`partners@abstractendeavors.com`)

## GitHub
https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_ai

## PyPi
https://pypi.org/project/abstract-ai/

## License 
MIT License

## Version
0.1.4.0

### Other scripts in same package

The module also consist of `endpoints.py`, `prompts.py`, `response_handling.py`, `tokenization.py`, scripts which provide additional functionalities to `abstract_ai` package.

