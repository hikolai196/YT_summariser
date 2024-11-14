import re
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

youtube_url = r"https://www.youtube.com/watch?v=DoMYrJQ8sSI"

# Function to get the video ID from a YouTube URL
def get_video_id(youtube_url):
    if 'youtube.com/watch?v=' in youtube_url:
        # Standard YouTube URL
        return youtube_url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in youtube_url:
        # Shortened YouTube URL
        return youtube_url.split('/')[-1]
    else:
        return print("Wrong URL format")

# Function to get the transcript of a YouTube video
def get_transcript(video_id):
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to clean the transcript
def clean_transcript(transcript):
    cleaned_transcript = []
    for entry in transcript:
        text = entry['text']
        # Remove unwanted tags like [Music], [Applause], etc.
        text = re.sub(r'\[.*?\]', '', text)
        # Remove extra whitespace
        text = text.strip()
        if text:  # Only add non-empty lines
            cleaned_transcript.append(text)
    return cleaned_transcript

# Function to get video details using yt_dlp
def get_video_details(youtube_url):
    ydl_opts = {
        'quiet': True,  # Suppress output
        'no_warnings': True  # Suppress warnings
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(youtube_url, download=False)
            video_details = {
                'title': info_dict.get('title', None),
                'description': info_dict.get('description', None),
                'publish_date': info_dict.get('upload_date', None),
                'author': info_dict.get('uploader', None),
                'length': info_dict.get('duration', None),
                'views': info_dict.get('view_count', None),
                'rating': info_dict.get('average_rating', None)
            }
            return video_details
        except Exception as e:
            print(f"Error: {e}")
            return None

# Combined function to save different types of content to a file
def save_to_file(content, filename, content_type):
    with open(filename, 'w', encoding='utf-8') as f:
        if content_type == 'transcript':
            for entry in content:
                start = entry['start']
                duration = entry['duration']
                text = entry['text']
                f.write(f"{start}s -- {start + duration}s\n{text}\n\n")
        elif content_type == 'cleaned_transcript':
            for line in content:
                f.write(f"{line}\n")
        elif content_type == 'video_details':
            f.write("Video Details\n")
            f.write(f"Title: \n{content['title']}\n\n")
            f.write(f"Description: \n{content['description']}\n\n")
            f.write(f"Publish Date: \n{content['publish_date']}\n\n")
            f.write(f"Author: \n{content['author']}\n\n")
            f.write(f"Length: \n{content['length']} seconds\n\n")
            f.write(f"Views: \n{content['views']}\n\n")
            f.write(f"Rating: \n{content['rating']}\n")

def main():
    
    video_id = get_video_id(youtube_url)
    
    if video_id:
        # Get video details
        video_details = get_video_details(youtube_url)
        if video_details:
            save_to_file(video_details, "infos.txt", 'video_details')
            print("Video details saved to infos.txt")
        else:
            print("Failed to get video details")
        
        # Get and save transcript
        transcript = get_transcript(video_id)
        if transcript:
            cleaned_transcript = clean_transcript(transcript)
            save_to_file(transcript, "transcript2.txt", 'transcript')
            save_to_file(cleaned_transcript, "cleaned_transcript2.txt", 'cleaned_transcript')
            print("Transcript saved to transcript2.txt and cleaned_transcript2.txt")
        else:
            print("Failed to get transcript")
    else:
        print("Invalid YouTube URL")

if __name__ == "__main__":
    main()