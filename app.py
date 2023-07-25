import gradio as gr
import sounddevice as sd
import wavio
import whisper
import numpy as np
from gtts import gTTS
from slyme import SlymeDriver
import time


model = whisper.load_model("base")

slyme = SlymeDriver(pfname='Default')
time.sleep(5)
slyme.select_latest_chat()
time.sleep(5)


def speech_to_text(audio_file):
    result = model.transcribe(audio_file)
    print(result)
    message = result["text"]
    lang = result["language"]
    return message, lang


def generate_answer(message):
    prompt = message
    output = slyme.completion(prompt)
    output = slyme.completion(prompt)
    print(output)

    # slyme.end_session()
    return output


def text_to_speech(text_data, lang):
    myobj = gTTS(text=text_data, lang=lang, slow=False)
    file = "welcome.wav"
    myobj.save(file)
    return file


def voice_bot(audio_data):
    question, lang = speech_to_text(audio_data)
    answer = generate_answer(question)
    audio_data = text_to_speech(answer, lang)
    return audio_data


# iface = gr.Interface(
#     fn=speech_to_text,
#     inputs=gr.Audio(source="microphone", type="filepath", label="Capture Audio"),
#     outputs=["text", "text"],
#     live=True,
# )


#iface = gr.Interface(
#      fn=generate_answer,
#      inputs="text",
#      outputs="text",
#)


# iface = gr.Interface(
#     fn=text_to_speech,
#     inputs=["text", "text"],
#     outputs=gr.Audio(),
# )


iface = gr.Interface(
    fn=voice_bot,
    inputs=gr.Audio(source="microphone", type="filepath", label="Capture Audio"),
    outputs=gr.Audio(),
)


if __name__ == "__main__":
    iface.launch(share=True)
