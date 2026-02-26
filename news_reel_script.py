"""
Instructions:

1. Install dependencies:
   pip install requests google-genai python-dotenv

2. Set environment variables (replace YOUR_KEYS):
   - On Windows (PowerShell):
       $env:NEWSAPI_KEY = "YOUR_NEWSAPI_KEY"
       $env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

   - On macOS/Linux (bash/zsh):
       export NEWSAPI_KEY="YOUR_NEWSAPI_KEY"
       export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

   You can also add these to your shell profile for persistence.
"""

import os
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
load_dotenv()

import requests
from google import genai


NEWS_API_URL = "https://newsapi.org/v2/everything"
NEWS_API_COUNTRY = "in"
DEFAULT_TOPIC = "Child Parenting In India"
GEMINI_MODEL_NAME = "gemini-3-flash-preview"


def fetch_news(topic: str, page_size: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch latest Indian news articles from NewsAPI for a given topic.

    - Filters by country = "in"
    - Sorts by published date (locally, descending)
    - Returns top 3 articles (after sorting)
    """
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        raise RuntimeError("Missing NEWSAPI_KEY environment variable.")

    params = {
        "q": topic,
        # "country": NEWS_API_COUNTRY,
        "apiKey": api_key,
    }

    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Error while calling NewsAPI: {e}") from e

    data = response.json()

    if data.get("status") != "ok":
        raise RuntimeError(f"NewsAPI returned error: {data.get('message')}")

    articles = data.get("articles", [])

    # Sort locally by publishedAt descending (newest first)
    def _published_at(article: Dict[str, Any]) -> str:
        return article.get("publishedAt") or ""

    articles_sorted = sorted(articles, key=_published_at, reverse=True)

    # Return top 3
    return articles_sorted[:3]


def format_articles(articles: List[Dict[str, Any]]) -> str:
    """
    Combine multiple articles into a clean, human-readable text block.
    """
    if not articles:
        return "No relevant articles were found."

    blocks = []
    for idx, article in enumerate(articles, start=1):
        title = article.get("title") or "No title"
        description = article.get("description") or ""
        content = article.get("content") or ""

        # Clean up: remove trailing '… [+123 chars]' that NewsAPI sometimes includes
        def _clean(text: Optional[str]) -> str:
            if not text:
                return ""
            return text.split(" [+", 1)[0].strip()

        description = _clean(description)
        content = _clean(content)

        parts = [f"Article {idx}:", f"Title: {title}"]
        if description:
            parts.append(f"Description: {description}")
        if content:
            parts.append(f"Content: {content}")

        blocks.append("\n".join(parts))

    return "\n\n".join(blocks)


def generate_summary(source_text: str, topic: str) -> str:
    """
    Use Gemini to generate a 120-150 word energetic reel-style summary.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY environment variable.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are writing a voiceover script for a short Instagram reel.

Topic: "{topic}"

Source news content:
\"\"\"
{source_text}
\"\"\"

Instructions:
- Write a single, tight script of 120-150 words.
- Use an energetic, engaging tone suitable for a fast-paced Instagram reel.
- Start with a strong hook in the very first sentence.
- Explain the key developments and why they matter, in simple language.
- Assume the audience is in India and generally aware of current events but not experts.
- Avoid filler phrases (like "in this video", "as you can see", "don't forget to like and subscribe").
- Avoid repetition and avoid mentioning that you are summarizing articles.
- Do not add hashtags, emojis, or calls to action; just the spoken script.

Now write the final script only.
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
        )
    except Exception as e:
        raise RuntimeError(f"Error while calling Gemini API: {e}") from e

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini API returned no text content.")

    # Clean up: replace em dashes with commas
    cleaned = text.strip().replace("—", ", ")
    return cleaned


def main() -> None:
    """
    Main entry point:
    - Use hard-coded topic
    - Fetch news
    - Format articles
    - Generate reel-style summary with Gemini
    - Print and save to reel_script.txt
    """
    # Hard-coded topic; change DEFAULT_TOPIC above if needed
    topic = DEFAULT_TOPIC

    try:
        articles = fetch_news(topic)
        if not articles:
            print("No articles found for that topic in India.")
            return

        formatted_articles = format_articles(articles)
        reel_script = generate_summary(formatted_articles, topic)

        # Output to console
        print("\n=== REEL SCRIPT ===\n")
        print(reel_script)
        print("\n===================\n")

        # Save to file
        output_path = "reel_script.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(reel_script)

        print(f"Reel script saved to '{output_path}'.")
    except RuntimeError as e:
        # Basic error handling with a clear message
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")


if __name__ == "__main__":
    main()

