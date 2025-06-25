import os
import re
import yt_dlp
import whisper
from langchain.tools import tool

AUDIO_DIR = "./audio"

def sanitize_filename(title: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", title)

@tool("transcribe_youtube", return_direct=True)
def transcribe_youtube(youtube_url: str) -> str:
    """
    Transcribes the audio of a YouTube video using OpenAI Whisper.
    Input: YouTube URL
    Output: Transcribed text
    """
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # Extract video info (title)
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            title = info["title"]
    except Exception as e:
        return f"Error: Failed to extract video info: {str(e)}"

    safe_title = sanitize_filename(title)
    audio_path = os.path.join(AUDIO_DIR, f"{safe_title}.mp3")
    transcript_path = os.path.join(AUDIO_DIR, f"{safe_title}.txt")

    # Download audio if not already present
    if not os.path.exists(audio_path):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': audio_path,
            'quiet': True,
            'no_warnings': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
        except Exception as e:
            return f"Error: Failed to download audio: {str(e)}"

    # Transcribe audio using Whisper
    try:
        if os.path.exists(transcript_path):
            with open(transcript_path, "r", encoding="utf-8") as f:
                transcript = f.read()
        else:
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            transcript = result["text"]
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(transcript)
    except Exception as e:
        return f"Error: Failed to transcribe audio: {str(e)}"

    return transcript