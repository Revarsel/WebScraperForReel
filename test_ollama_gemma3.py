"""
Quick test script for running Gemma 3 12B locally via Ollama.

Prerequisites:
- Ollama installed and running (with AMD GPU support).
- Model pulled (first time):
    ollama run gemma3:4b
"""

import ollama

MODEL_NAME = "gemma3:4b"


def generate_summary_with_ollama(source_text: str, topic: str) -> str:
    prompt = f"""You are writing a voiceover script for a short Instagram reel.

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
- Avoid filler phrases and repetition.
- Do not add hashtags, emojis, or calls to action at all; just the spoken script.
"""

    resp = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
    )

    text = resp.get("response", "")
    if not text:
        raise RuntimeError("Ollama returned an empty response.")

    # Replace em/en dashes, keep normal hyphens
    cleaned = text.strip().replace("—", ", ").replace("–", ", ")
    return cleaned


def main() -> None:
    # Simple dummy source text for testing;
    # you can paste your formatted news block here instead.
    topic = "AI policy in India"
    source_text = """
India is rapidly evolving its AI policy landscape, with new guidelines,
regulatory frameworks, and innovation incentives. Policymakers are
balancing innovation, data privacy, and ethical AI use while encouraging
startups and global companies to invest in the Indian AI ecosystem.
"""

    try:
        reel_script = generate_summary_with_ollama(source_text, topic)
        print("\n=== REEL SCRIPT (OLLAMA / GEMMA3:12B) ===\n")
        print(reel_script)
        print("\n=========================================\n")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

