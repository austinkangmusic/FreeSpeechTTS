import ollama
from utils import files
from run_ollama1 import start_ollama

def stream_chatbot_response(message):
    stream = ollama.chat(
        model=model,
        messages=message,
        # format='json',
        stream=True,
    )
    response = ''
    print('\nAI:')
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
        response += chunk['message']['content']  # Concatenate the content, not the whole chunk
    print('\n')
    return response

conversation_history = []
system_prompt = files.read('prompts/system_prompt.md')
model = "llama3.2:1b"
start_ollama(model) 

while True:
    # print(full_prompt)
    user_input = input('User:\n')
    conversation_history.append({'role': 'user', 'content': user_input})
    full_prompt = conversation_history
    print(full_prompt)
    ai_output = stream_chatbot_response(full_prompt)
    conversation_history.append({'role': 'ai', 'content': ai_output})

