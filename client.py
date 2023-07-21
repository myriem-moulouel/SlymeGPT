import socket
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

import whisper

def start_client():
    host = '127.0.0.1'  # Server IP address
    port = 12345       # Port to connect to

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:

        start = input("start recording ? click Enter ----- you have 10seconds (ASK YOUR QUESTION)")

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



        # Recognize speech using openai Web Speech API
        model = whisper.load_model("base")

        result = model.transcribe("recording.wav")
        message = result["text"]

        print("You said: " + message)

        client_socket.sendall(message.encode('utf-8'))
        data = client_socket.recv(1024).decode('utf-8')
        print("Received from server: {}".format(data))


    client_socket.close()

if __name__ == "__main__":
    start_client()

