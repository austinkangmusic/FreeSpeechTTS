from ollama import Client
from dotenv import load_dotenv
import os
import subprocess

load_dotenv

command = os.getenv('OLLAMA_EXE_PATH')

def setup_client(model: str, host_url: str):
    """
    Sets up the environment and client for connecting to the Ollama model.
    Pulls the specified model from Ollama if necessary.

    Args:
        model (str): The model identifier to pull.
        host_url (str): The host URL for the Ollama client.
    
    Returns:
        Client: The initialized Ollama client.
    """
    # Set the environment variable for the host
    os.environ['OLLAMA_HOST'] = host_url

    # Create and return the client after setting the environment variable
    client = Client(
        host=os.environ['OLLAMA_HOST']
    )

    # Run the `ollama` command to pull the model
    subprocess.run(
        [command, 'pull', model],
        env={**os.environ}  # Ensure the environment variable is available to the subprocess
    )

    return client
