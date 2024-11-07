import yt_dlp
import whisper
import os

def download_audio_from_youtube(youtube_url, output_filename="audio.mp3"):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        # Adjust filename if yt-dlp appends '.mp3' again
        if not os.path.isfile(output_filename) and os.path.isfile(output_filename + ".mp3"):
            os.rename(output_filename + ".mp3", output_filename)

        return output_filename
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

def transcribe_audio_to_text(audio_file_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    return result["text"]

def save_text_to_file(text, file_path="transcription.txt"):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

def youtube_to_text(youtube_url, audio_filename="audio.mp3", text_filename="transcription.txt"):
    audio_file_path = download_audio_from_youtube(youtube_url, audio_filename)
    
    if audio_file_path is None or not os.path.isfile(audio_file_path):
        print("Failed to download audio or audio file not found.")
        return

    transcription_text = transcribe_audio_to_text(audio_file_path)
    save_text_to_file(transcription_text, text_filename)
    
    os.remove(audio_file_path)
    print(f"Transcription saved to {text_filename}")

# Example usage
youtube_url = "https://www.youtube.com/watch?v=I-sH53vXP2A"
youtube_to_text(youtube_url)
