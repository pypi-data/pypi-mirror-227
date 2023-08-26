# Judini Python Package

This package provides you with an easy way to interact with the Judini API in your Python applications.

## Install

To install the package, simply run the following command:

```bash
pip install judini
```

## Usege

Below is a sample code demonstrating how to use the Judini package in your Python application:

```python

# Import the package
import asyncio
from judini.codegpt.agent import Agent

def main():
    # Replace with your actual API key and URL ID
    api_key = "your_api_key_here"
    agent_id = "your_agent_id_here"

    # Initialize the CODEGPT class
    agent_instance = Agent(api_key, agent_id)

    # Optional: update API key or URL ID if needed
    agent_instance.set_api_key("new_api_key")
    agent_instance.set_agent_id("new_agent_id")

    # Create the prompt
    prompt = "tell me a short story about a blue turtle"

    # Make a completion request
    response = asyncio.run(agent_instance.completion(prompt, stream=False))

    # Handle the response as needed
    print(response)

if __name__ == "__main__":
    main()
```
