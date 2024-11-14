import os
import ollama

# Path to the transcription file
TRANSCRIPTION_FILE = r"transcription.txt"

# Function to summarize transcription using Ollama
def summarize_transcription():
    if not os.path.isfile(TRANSCRIPTION_FILE):
        raise FileNotFoundError(f"{TRANSCRIPTION_FILE} not found.")

    # Read the transcribed text
    with open(TRANSCRIPTION_FILE, 'r') as file:
        transcript = file.read()

    if len(transcript) == 0:
        print("The transcription file is empty.")
        return

    # Prepare the prompt for summarization
    prompt = f"Please summarize the following context and give some points if possible:\n\n{transcript}"

    summary = ollama.generate('llama3.2', prompt)
    print("Summary:", summary['response'])

    # Save the summary to a text file
    with open("summary.txt", 'w') as file:
        file.write(summary['response'])

    print("Summary saved to summary.txt")

if __name__ == "__main__":
    summarize_transcription()