from faster_whisper import WhisperModel
from ...cuda_device import get_device
from dotenv import load_dotenv
import os

load_dotenv()
whisper_model_size = os.getenv('whisper_model_size')

def initialize_whisper_model():
    device = get_device()  # Dynamically select device using cuda_device.py
    model_size = f"{whisper_model_size}"
    
    # Initialize Whisper model
    whisper_model = WhisperModel(model_size, device=device, compute_type="float32")
    
    return whisper_model
