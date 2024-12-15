from faster_whisper import WhisperModel
from ...cuda_device import get_device
from dotenv import load_dotenv
import os

load_dotenv()
whisper_model_size = os.getenv('whisper_model_size')

def initialize_whisper_model():
    device = get_device()  # Dynamically select device using cuda_device.py
    print(f"Loading '{whisper_model_size}' model...")
    
    # Provide the path to your local model directory
    model_path = f"faster_whisper_models/{whisper_model_size}"
    
    # Initialize Whisper model with the local path
    whisper_model = WhisperModel(model_path, device=device, compute_type="float32")
    
    return whisper_model
