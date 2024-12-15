import time
import threading
from dotenv import load_dotenv
from ollama import Client
from run_ollama import setup_client
from pydantic import BaseModel
from typing import List, Optional, Dict
from utils.extractor import extract_values
from utils import files, timer, play_audio
from utils.human_voice_transcriber.whisper import initialize_whisper, voice_transcriber

use_low_tts = True

if use_low_tts:
    from utils.ai_voice_generator.pyttxs3 import generate_pyttxs3_voice, initialize_pyttsx3
else:
    from utils.ai_voice_generator.xttsv2 import initialize_xttsv2, generate_xttsv2_voice

model = 'llama3.1:8b'
host_url = os.getenv('host_url')
client = setup_client(model, host_url)
system = files.read('prompts/system_prompt.md')
user_info = files.read('user/user_info.md')
personality = files.read(f"XTTS-v2_models/XTTS-v2_PeterJarvis/personality/PeterJarvis.md")

conversation_history_json = []
conversation_history = ''


from typing import List, Optional
from pydantic import BaseModel, field_validator

class Communication(BaseModel):
    thoughts: List[str]  # Explain the reasoning behind the response
    metathoughts: List[str]  # Explain the reasoning behind the response
    action: str  # The action to take, e.g., respond, listen, etc.
    message: Optional[str]  # Text to communicate or None if no message

class SpeechControl(BaseModel):
    thoughts: List[str]  # Explain the reasoning behind continuing or stopping
    metathoughts: List[str]  # Reflect on the broader context of the speech
    action: str  # The action to take: 'continue' or 'stop'    

def get_response(prompt):
    output = client.chat(
        messages=prompt,
        model=model,
        format=Communication.model_json_schema(),
        options={'temperature': 0}  # Set temperature to 0 for more deterministic output
    )

    full_response = Communication.model_validate_json(output.message.content)

    return full_response

def get_speech_control_response(prompt):
    output = client.chat(
        messages=prompt,
        model=model,
        format=SpeechControl.model_json_schema(),
        options={'temperature': 0}  # Set temperature to 0 for more deterministic output
    )

    full_response = SpeechControl.model_validate_json(output.message.content)

    return full_response

def llm_run():
    global conversation_history

    while True:
        with open("transcription/input.txt", "r") as file:
            user_input = file.read()
        if user_input == '':
            user_input = '[No Input]'
            
        system_prompt = f'{personality}\n\n{system}\n\n{user_info}\n\n##CONVERSATION HISTORY:\n{conversation_history}'

        full_prompt = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_input}]

        ai_response = get_response(full_prompt)

        print('='*180, f'\n{ai_response}\n')

        # Specify the keys you want to extract
        keys_of_interest = ['thoughts', 'action', 'message']
        thoughts, action, message = extract_values(ai_response, keys_of_interest)
        if 'respond' in action or 'interrupt' in action:
            if user_input == '':
                conversation_history_json.append({'role': 'user', 'content': '[No Input]'})
            else:
                conversation_history_json.append({'role': 'user', 'content': user_input})
            conversation_history_json.append({'role': 'assistant', 'content': message})
            with open("statuses/chatbot_replied.txt", "w") as file:
                file.write('true')   

        if 'ignore' in action or 'wait' in action or 'listen' in action:
            if '[Not Speaking]' in user_input:
                timer.start_time()


                current_time = timer.get_elapsed_time()
                if current_time >= 5:
                     conversation_history_json.append({'role': 'user', 'content': user_input})
                     conversation_history_json.append({'role': 'assistant', 'content': f'[{action}]'})
                     with open("statuses/chatbot_replied.txt", "w") as file:
                         file.write('true')   
                     timer.reset_time()

        print('AI: ', message)
    
        # Formatting the conversation
        formatted_conversation = []
        for entry in conversation_history_json:
            if entry['role'] == 'user':
                # Remove trailing "[Not Speaking]" or "... [Speaking]"
                cleaned_content = entry['content'].replace("[Not Speaking]", "").replace("... [Still Speaking]", "—").strip()
                formatted_conversation.append(f"USER: {cleaned_content}")
            elif entry['role'] == 'assistant':
                formatted_conversation.append(f"ASSISTANT: {entry['content']}")

        # Join the formatted lines into a single string
        conversation_history = "\n".join(formatted_conversation)
        with open("conversation_history.txt", "w") as file:
            file.write(conversation_history)   

        if message is None:
            pass
        else:
            try:
                with open("transcription/output.txt", "w") as file:
                    file.write(message)   
            except Exception as e:
                print("Error writing to file: ", e)

            if use_low_tts:
                generate_pyttxs3_voice.run()
            else:
                generate_xttsv2_voice.run()

            play_audio.run()


def main():
    transcribe = threading.Thread(target=voice_transcriber.execute)
    transcribe.start()
    llm_run()


def input_simulation():
    global playback_active
    while True:
        time.sleep(1)
        # Given sentence
        sentence = input("\nUser:\n")

        if sentence != '':
            with open("statuses/chatbot_replied.txt", "w") as file:
                file.write('false')

        # Get start and end times

        # Split the sentence into words
        words = sentence.split()

        # Initialize an empty string to build the output
        current_content = ""

        for word in words:

            # Add the next word to the current content
            current_content += word + " "

            # Open the file in write mode and overwrite it with the current content
            with open("transcription/input.txt", "w") as file:
                file.write(current_content.strip() + f"... [Still Speaking]")  # Add [Speaking] after each incremental addition
            
            time.sleep(0.25)  # Wait 2 seconds before adding the next word


        # Open the file in write mode and overwrite it with the current content
        with open("transcription/input.txt", "w") as file:
            file.write(current_content.strip() + f" [Not Speaking]")

        def input_threading_lol():
            while True:
                with open('transcription/input.txt', 'r') as file:
                    user_input = file.read()
                with open('statuses/speak_status.txt', 'r') as file:
                    speak_status = file.read()
                with open('statuses/chatbot_replied.txt', 'r') as file:
                    chatbot_replied = file.read()
                if speak_status == 'false' and chatbot_replied == 'true' and '[Not Speaking]' in user_input:

                    with open("transcription/input.txt", "w") as file:
                        file.write('')  
        input_lol = threading.Thread(target=input_threading_lol)
        input_lol.start()

def main_input_simulator():
    input_thread = threading.Thread(target=input_simulation)
    input_thread.start()
    llm_run()

main()
# main_input_simulator()










