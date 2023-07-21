import websocket
import pyttsx3


import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

import whisper



def on_message(ws, message):
    # Receive the chatbot's response as text from the server
    print(f"Chatbot says: {message}")
    # Convert the chatbot's response from text to audio
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection established")





    # Sampling frequency
    freq = 44100
    
    # Recording duration
    duration = 10
    
    # Start recorder with the given values
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq),
                    samplerate=freq, channels=2)
    
    # Record audio for the given number of seconds
    sd.wait()
    
    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    write("recording.wav", freq, recording)

    model = whisper.load_model("base")

    result = model.transcribe("recording.wav")
    ws.send(result["text"])
    ws.close()



if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

