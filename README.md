# YouTube Transcription Summarizer

## Overview
A Python-based tool that transforms YouTube video content into concise, readable summaries through advanced speech recognition and large language model technologies.

One can use: 

  `step1_transcribe_w_audio.py`

then

  `step2_summarize.py`

for summarization.

Where AI agent: 

  `langgraphflow.py`

Binding the tools

  `transcribe_tool.py
  summarize_agent.py`

is also available. 

## Features
- Multilingual Speech-to-Text Conversion
- Intelligent Content Summarization
- Configurable Summary Length
- Supports Multiple Transcription Methods

## Technical Architecture
- **Speech Recognition**: OpenAI Whisper
- **Summarization**: Ollama + Prompt Engineering
- **Languages**: Python

## Prerequisites
- Python 3.11+
- Ollama is installed locally
- pip install requirements.txt

## Installation
```bash
git clone https://github.com/[your-username]/youtube-transcription-summarizer
cd youtube-transcription-summarizer
pip install -r requirements.txt
