from .robotic_voice import if_robotic, apply_vocoder
from utils.C3PO_effect import apply_c3po_effect
import wave
import pyaudio
import os

buffer = b''  # Buffer to store audio data
wf_global = None  # To keep a reference to the wave file object
speak_status = True
playback_active = False

def play(file_path):
    global buffer, wf_global, speak_status, playback_active
    speak_status = True
    playback_active = True
    with open("statuses/playback_active.txt", "w") as file:
        file.write('true')   
    if not os.path.exists(file_path):
        print(f"Audio file not found: {file_path}")
        return

    wf = wave.open(file_path, 'rb')
    wf_global = wf
    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        data = wf.readframes(512)
        while data and speak_status:
            buffer += data
            stream.write(data)
            data = wf.readframes(512)
        
        playback_active = False
        with open("statuses/playback_active.txt", "w") as file:
            file.write('false')   
        # print("AI has stopped talking.")

        buffer = b''  # Clear buffer after saving if needed
        
        stream.stop_stream()
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        stream.close()
        wf.close()
        p.terminate()

def run():
    if if_robotic:
        apply_c3po_effect("audios/output.wav", "audios/output_c3po_effect.wav")
        play("audios/vocoder_output.wav")
    else:
        apply_c3po_effect("audios/output.wav", "audios/output_c3po_effect.wav")
        play("audios/output_c3po_effect.wav")