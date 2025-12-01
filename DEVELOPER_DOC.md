# YouTube Video Analyzer — Developer Notes

A small Streamlit app that classifies a YouTube video as **educational** or **entertainment**, then runs a set of Gemini-powered tools to summarize it. The core logic lives in `youtube.py`; `app.py` provides the UI.

## Architecture
- Single-file friendly: the UI and backend logic can live together in `app.py` (Streamlit handles input, transcript fetch, classification, and rendering).
- Helper module (`youtube.py`): currently holds the transcript fetch, Gemini classification, and tool wiring (`FunctionTool`, `FunctionCallingAgentWorker`). You can inline this into `app.py` to keep everything in one file.
- Tools (`llama_index`):
  - Educational: `GenerateTitle`, `SummarizeTopics`, `FindPrerequisites`.
  - Entertainment: `IdentifyGenre`, `SuggestAgeGroup`, `EntertainmentSummary` (150-word summary).
- Transcript source: `youtube_transcript_api.YouTubeTranscriptApi.get_transcript` (no audio download).
- Secrets loading: `python-dotenv.load_dotenv` for `GEMINI_API_KEY`.

## Project Structure
```
app.py             # Streamlit UI + backend (can inline helpers here)
youtube.py         # Helper module for LLM + transcript logic (optional if inlined)
requirements.txt   # Python deps
Dockerfile         # Container build (kept for convenience; docs focus on local use)
README.md          # User-facing setup/run notes
DEVELOPER_DOC.md   # Developer notes (this file)
```

## Data/Execution Flow
1. UI (`streamlit`): user enters a video ID.
2. Transcript fetch (`youtube_transcript_api`): `get_transcript(video_id)` pulls captions and concatenates them.
3. Classification (`llama_index.llms.gemini`): `classify(transcript)` prompts Gemini to return `educational` or `entertainment` (fallback `unknown`).
4. Tool selection (`llama_index.core.tools` + `llama_index.core.agent`): choose tool set based on classification and run each tool on the transcript text.
5. Presentation (`streamlit`): results are rendered in the UI.

## Environment & Secrets
- Required: `GEMINI_API_KEY` (load via `.env` or environment variable). No other secrets.
- Network calls: YouTube Transcript API + Gemini API (costs apply).

## Local Development
- Python 3.10 recommended (matches `python:3.10-slim` in the Dockerfile).
- Setup
  ```bash
  python -m venv .venv
  .venv/Scripts/activate  # PowerShell: .venv\\Scripts\\Activate.ps1
  pip install -r requirements.txt
  ```
- Run the app
  ```bash
  streamlit run app.py
  ```
- Run with Docker
  ```bash
  docker build -t youtube-analyzer .
  docker run -p 8501:8501 --env-file .env youtube-analyzer
  ```

## Notes & Gotchas
- The UI includes emoji markers; if they render as garbled characters on Windows consoles, swap them for plain text.
- `youtube.py` currently imports and executes with a default `video_id` at module import time; when using it as a library, ensure you call `get_transcript`/`classify` with your own ID before using the tools.
- Error handling is minimal; transcripts for disabled/auto-generated captions may fail and raise exceptions.
- No persistence or caching; each request re-fetches the transcript and calls Gemini.

## Extension Ideas
- Add retries and clearer errors when transcripts are unavailable.
- Add rate limiting and lightweight caching for transcripts/LLM calls.
- Expose a small API endpoint (e.g., FastAPI) for programmatic use.
- Improve the classification prompt and add guardrails for non-English content.
