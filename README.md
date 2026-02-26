# News Reel Script (India)

This project contains a small Python script that fetches the latest Indian news on a specific topic and turns it into a short Instagram reel–style voiceover script using the Gemini API.

## What the script does

- **Fetches news from NewsAPI**
  - Uses the `everything` endpoint on NewsAPI.
  - Reads your NewsAPI key from the `NEWSAPI_KEY` environment variable (loaded from `.env`).
  - Searches for a **hard-coded topic** (configured as `DEFAULT_TOPIC` in `news_reel_script.py`).
  - Sorts the articles by `publishedAt` (newest first) and keeps the **top 3**.
  - Extracts the **title**, **description**, and **content** from each article.
  - Combines them into a single clean text block.

- **Summarizes with Gemini (google-genai)**
  - Uses the new `google.genai` SDK, via `from google import genai`.
  - Reads your Gemini API key from the `GEMINI_API_KEY` environment variable (loaded from `.env`).
  - Calls the `gemini` model with a prompt that:
    - Produces a **120–150 word** summary.
    - Uses an **energetic, engaging tone** suitable for an Instagram reel.
    - Starts with a **strong hook** in the first sentence.
    - Explains the key developments in **simple, clear language** for an Indian audience.
    - Avoids filler, repetition, hashtags, emojis, and calls to action.
  - Cleans up the final text by replacing **em/en dashes with commas** before returning.

- **Outputs the final script**
  - Prints the finished reel script to the console.
  - Saves it to `reel_script.txt` in the project root.

## Requirements

- Python 3.9+ (recommended)
- Dependencies:
  ```bash
  pip install requests google-genai python-dotenv
  ```

## Environment variables

Create a `.env` file in the project root (this file is **ignored by git**) with:

```env
NEWSAPI_KEY=your_newsapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

The script uses `python-dotenv` to load these automatically.

## How to run

From the project root:

```bash
python news_reel_script.py
```

The topic is hard-coded in `news_reel_script.py` as `DEFAULT_TOPIC`.  
To change what news the reel is based on, edit that constant and run the script again.

