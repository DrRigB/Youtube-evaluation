import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv('ApiKey.env')
openai_api_key = os.getenv("YOUR_API_KEY_HERE")  # Make sure this matches the env variable

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Define audio output path
speech_file_path = Path(__file__).parent / "summary_output.mp3"

# Read transcription text
def read_transcription(file_path="transcription.txt"):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("Transcription file not found.")
        return None

# Generate summary
def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": """You are witty in your responses. You are the best summarizer. 
                   You also add jokes in between with a little chuckle after you tell them."""},
                  {"role": "user", "content": text}]
    )
    return response.choices[0].message.content

# Convert text to speech
def text_to_speech(text, selected_voice, output_path):
    try:
        audio_response = client.audio.speech.create(
            model="tts-1",
            voice=selected_voice,
            input=text
        )
        audio_data = audio_response.content
        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_data)
        print(f"Speech saved to {output_path}")
        play_audio(output_path)
    except Exception as e:
        print(f"Error generating speech: {e}")

# Play audio file
def play_audio(file_path):
    try:
        if os.name == 'nt':
            os.startfile(file_path)
        elif os.name == 'posix':
            subprocess.run(['open', file_path])  # macOS
        else:
            print("Unsupported OS for audio playback.")
    except Exception as e:
        print(f"Error playing audio: {e}")

# Set selected voice and run sequence
selected_voice = "onyx"
def run():
    transcription_text = read_transcription("transcription.txt")
    if not transcription_text:
        return
    summary_content = summarize_text(transcription_text)
    print("Generated Summary:", summary_content)
    text_to_speech(summary_content, selected_voice, speech_file_path)
    print("Summary audio generated.")

if __name__ == "__main__":
    run()
