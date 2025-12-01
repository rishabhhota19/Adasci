# YouTube Video Analyzer

Classifies a YouTube video as **educational** or **entertainment** and summarizes it with Gemini. Keep it simple: UI and backend logic live together in one Streamlit script.

## What It Does
- Fetches captions for a YouTube video ID (no audio download).
- Uses Gemini to classify as `educational` or `entertainment`.
- Educational output: title, key topics, prerequisites.
- Entertainment output: genre, suitable age group, 150-word summary.

## Quickstart (Local)
1. Install Python 3.10+ and create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your Gemini key (e.g., `.env`):
   ```
   GEMINI_API_KEY=your_key_here
   ```
4. Run Streamlit:
   ```bash
   streamlit run app.py
   ```

## Notes
- Single-file friendly: keep UI + logic in `app.py`. If you split helper functions into another module, update the imports accordingly.
- Network is required for YouTube transcripts and Gemini API.
- Error handling is minimal; missing captions or API issues will raise exceptions.
