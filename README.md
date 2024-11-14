# YT_summariser
YouTube summarizer using Python
## This project is separated into two steps:
### Step1. Get transcription
1.  The one with audio uses the yt library to download YouTube audio, transcribed using OpenAI Whisper.Therefore, the transcription looks like a normal paragraph.
2.  The one with transcription directly downloads the transcription using the transcript API. However, the transcription is separated line by line.
  ---
### Step2. Summarize the transcription with text-to-text LLM via Ollama.
  Remember to install Ollama in the computer before using it. Or it will fail.
