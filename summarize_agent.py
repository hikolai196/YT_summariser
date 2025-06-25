import ollama
from langchain.tools import tool

@tool("summarize_transcript", return_direct=True)
def summarize_transcript(transcript: str) -> str:
    """
    Summarizes a given transcript string using Ollama (e.g. phi3.5).
    Returns a well-structured Markdown summary.
    """
    if not transcript.strip():
        return "Error: Transcript is empty."

    prompt = f"""
    You are an expert summarizer. Your task is to generate a structured and well-formatted summary report in **Markdown format** based on the following transcription.

    ## Instructions:
    - Use proper Markdown syntax, including `#` for headings, `**bold**` for emphasis, and `-` or `1.` for lists.
    - Structure the summary clearly with appropriate headers and bullet points.
    - Maintain readability and professionalism.

    ## Expected Markdown Structure:
    # [Title]

    ## Introduction
    Briefly introduce the content, including the main topic and purpose.

    ## Key Points
    - Summarize key insights using bullet points.
    - Keep points concise and well-structured.

    ## Detailed Sections
    ### [Subheading 1]
    - Provide relevant details.

    ### [Subheading 2]
    - Continue breaking down key aspects.

    ## Conclusion
    Summarize the main takeaways in a few sentences.

    ### Transcription Content:
    {transcript}
    """

    try:
        response = ollama.generate(model='phi4-mini', prompt=prompt)
        summary_text = response.get("response", "").strip()
        return summary_text or "Error: Summary was empty."
    except Exception as e:
        return f"Error: Failed to summarize transcript: {str(e)}"