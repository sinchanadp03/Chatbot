import gradio as gr
import google.generativeai as palm
import os
import numpy as np
import speech_recognition as sr

ffmpeg_directory = "C:\\Users\\HP\\miniconda3\\envs\\myenvironment\\Lib\\site-packages\\ffmpeg\\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_directory
palm.configure(api_key="AIzaSyDhlCsSzXOcaZ2SHnFSEFCGSI-BgHqsMcU")

model = "models/text-bison-001"

def generate_output(input_text):
    prompt = f"""You will help me in education and give only precised answer for the {input_text}"""
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.3,
        max_output_tokens=2048,
    )
    return completion.result

# Define a function to handle both text and voice input
def handle_input(input_text, voice_input):
    print("Type of voice_input:", type(voice_input))
    print("Voice input contents:", voice_input)

    if voice_input and len(voice_input) == 2:
        sample_rate, audio_data = voice_input
        if isinstance(audio_data, np.ndarray):
            sample_width = audio_data.dtype.itemsize  # Determine the sample width based on the data type.
            audio_bytes = audio_data.tobytes()
            recognizer = sr.Recognizer()
            audio = sr.AudioData(audio_bytes, sample_rate=sample_rate, sample_width=sample_width)
            try:
                audio_text = recognizer.recognize_google(audio)
                return generate_output(audio_text)
            except sr.UnknownValueError:
                return "Voice input not recognized."
    if input_text:
        return generate_output(input_text)
    else:
        return "No input provided."
    pass

iface = gr.Interface(
    fn=handle_input,
    inputs=[gr.Textbox(), gr.Audio(label="Ask your question by voice:")],  # Removed 'source' keyword
    outputs="text",
    title="EDU.GPT",
)

iface.launch()
