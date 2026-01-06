video_id = "pTFZFxd4hOI"

import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Document
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import FunctionAgent
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
MODEL_NAMES = [
    "gemini-pro",
    "gemini-1.0-pro",
    "gemini-1.5-pro",
    "gemini-2.0-pro",
    "gemini-3.0-pro",
    "models/gemini-pro",
    "models/gemini-1.0-pro",
    "models/gemini-1.5-pro",
    "models/gemini-2.0-pro",
    "models/gemini-3.0-pro"
]

llm = GoogleGenAI(model="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))

def get_transcript(video_id: str) -> str:
    transcript_list = YouTubeTranscriptApi().fetch(video_id)
    return " ".join([snippet.text for snippet in transcript_list])

# transcript = get_transcript(video_id)
# doc = Document(text=transcript)

def classify(transcript: str) -> str:
    res = llm.complete(
        f'''Classify the transcript strictly as one of the following:
    - educational
    - entertainment
        transcript:\n\n{transcript[:2000]}'''
    ).text.strip().lower()
    return res if res in ("educational", "entertainment") else "unknown"

# classification = classify(doc.text)
# Define educational tools
tools_edu = [
    FunctionTool.from_defaults(
        fn=lambda txt: llm.complete(f"Title for educational video:\n{txt}").text.strip(),
        name="GenerateTitle",
        description="Create a title for educational videos"
    ),
    FunctionTool.from_defaults(
        fn=lambda txt: llm.complete(f"List key topics:\n{txt}").text.strip(),
        name="SummarizeTopics",
        description="Summarize topics covered"
    ),
    FunctionTool.from_defaults(
        fn=lambda txt: llm.complete(f"List prerequisites:\n{txt}").text.strip(),
        name="FindPrerequisites",
        description="List prerequisites for understanding"
    ),
]

# Define entertainment tools
tools_ent = [
    FunctionTool.from_defaults(
        fn=lambda txt: llm.complete(f"Identify genre:\n{txt}").text.strip(),
        name="IdentifyGenre",
        description="Identify the entertainment genre"
    ),
    FunctionTool.from_defaults(
        fn=lambda txt: llm.complete(f"Suggest age group:\n{txt}").text.strip(),
        name="SuggestAgeGroup",
        description="Recommend suitable age group"
    ),
    FunctionTool.from_defaults(
        fn=lambda txt: llm.complete(f"150-word summary:\n{txt}").text.strip(),
        name="EntertainmentSummary",
        description="Provide a 150-word summary"
    ),
]

# Choose tools based on classification

# Execution block removed to prevent running on import
if __name__ == "__main__":
    print("Running test execution...")
    # You can put the test logic here if needed
    pass
