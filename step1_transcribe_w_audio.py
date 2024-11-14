import yt_dlp
import whisper
import os

AUDIO_DIR = r"./audio"
youtube_url = "link_here"

# Get video information
def get_video_info(youtube_url):
    # Options for not downloading the video but extracting info
    ydl_opts = {
        'quiet': True,  # Suppress output
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract information from the YouTube URL
        info = ydl.extract_info(youtube_url, download=False)
    
    # Return the info dictionary
    return info

# Function to download audio to a specified directory
def download_audio_with_ytdlp(youtube_url, video_info):
    # Ensure the directory exists
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    # Set the output template with the custom save directory and video title
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(AUDIO_DIR, f"{video_info['title']}.%(ext)s"), 
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    filepath = os.path.join(AUDIO_DIR, f"{video_info['title']}.mp3")
    return filepath

def stt(filepath):
    # Load the Whisper model
    model = whisper.load_model("base")

    # Transcribe the audio file
    result = model.transcribe(filepath)
    transcription = result["text"]

    # Save the transcription to a text file
    with open(r"transcription.txt", 'w') as f:
        f.write(transcription)
    
    if os.path.isfile("transcription.txt"):
        print("File processed.")

def main():
    video_info = get_video_info(youtube_url)
    filepath = download_audio_with_ytdlp(youtube_url,video_info)
    # print(filepath)
    stt(filepath)

if __name__ == "__main__":
    main()