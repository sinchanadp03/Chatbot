import gradio as gr
import google.generativeai as palm
import os
import numpy as np
import speech_recognition as sr

ffmpeg_directory = "C:\\Users\\HP\\miniconda3\\envs\\myenvironment\\Lib\\site-packages\\ffmpeg\\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_directory
api_key="Your API Key"

palm.configure(api_key=api_key)

# Instantiate the model
model = palm.GenerativeModel('gemini-1.5-flash')

def generate_output(input_text):
    try:
        # List methods and attributes to understand what is available
        # print("Model attributes and methods:", dir(model))
        
        # Use the correct method signature based on model's documentation
        # If generate_content has different parameters, adapt here
        completion = model.generate_content(input_text)  # Adjust as per correct usage
        return completion.text if hasattr(completion, 'text') else str(completion)
    except Exception as e:
        return f"An error occurred: {e}"

def handle_input(input_text, voice_input):
    if voice_input and len(voice_input) == 2:
        sample_rate, audio_data = voice_input
        if isinstance(audio_data, np.ndarray):
            sample_width = audio_data.dtype.itemsize  # Determine the sample width based on the data type
            audio_bytes = audio_data.tobytes()
            recognizer = sr.Recognizer()
            audio = sr.AudioData(audio_bytes, sample_rate=sample_rate, sample_width=sample_width)
            try:
                audio_text = recognizer.recognize_google(audio)
                return generate_output(audio_text)
            except sr.UnknownValueError:
                return "Voice input not recognized."
            except sr.RequestError as e:
                return f"Error with the speech recognition service: {e}"
    
    if input_text:
        return generate_output(input_text)
    else:
        return "No input provided."

iface = gr.Interface(
    fn=handle_input,
    inputs=[gr.Textbox(label="Text Input"), gr.Audio(label="Ask your question by voice:")],
    outputs="text",
    title="EDU.GPT",
)

if _name_ == "_main_":
    iface.launch()
