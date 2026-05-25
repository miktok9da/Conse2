"""
Generate new topics using AI when topics.txt runs low.

This script:
1. Checks if topics.txt has enough topics (< 50 remaining)
2. Generates 100 new unique topics using Pollinations AI
3. Appends them to topics.txt
"""

import os
import requests
from urllib.parse import quote
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_new_topics(count=100):
    """Generate new French topics about ancient women using paid Pollinations API."""

    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        raise ValueError("POLLINATIONS_API_KEY environment variable is required for paid API")

    system = (
        "Tu es un historien spécialisé dans l'histoire des femmes dans les civilisations anciennes. "
        f"Crée une liste de {count} sujets uniques en français. "
        "Chaque sujet doit être court (5-10 mots), intéressant et éducatif. "
        "Les sujets doivent couvrir : les lois, les coutumes, les femmes célèbres, les professions, la religion, la culture, l'art. "
        "Ne produis QUE les sujets, un par ligne, sans numéros ni marqueurs."
    )

    prompt = f"Crée {count} sujets uniques sur les femmes dans les civilisations anciennes"

    url = f"https://gen.pollinations.ai/text/{quote(prompt)}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "model": "nova-fast",
        "temperature": 0.9,
        "system": system,
        "json": False
    }

    print(f"[topics] Generating {count} new French topics...")
    r = requests.get(url, headers=headers, params=params, timeout=120)
    r.raise_for_status()
    
    # Parse topics
    topics = []
    for line in r.text.strip().split('\n'):
        # Remove numbering and clean
        cleaned = line.strip()
        # Remove common prefixes
        for prefix in ['- ', '* ', '• ']:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
        # Remove numbering like "1. " or "1) "
        import re
        cleaned = re.sub(r'^\d+[\.\:]\s*', '', cleaned)
        
        if cleaned and len(cleaned) > 5:
            topics.append(cleaned)
    
    return topics[:count]

def check_and_update_topics():
    """Check topics.txt and add more if needed."""
    
    topics_file = Path('topics.txt')
    
    # Read existing topics
    if topics_file.exists():
        with open(topics_file, 'r', encoding='utf-8') as f:
            existing_topics = [line.strip() for line in f if line.strip()]
    else:
        existing_topics = []
    
    print(f"[topics] Current topics: {len(existing_topics)}")
    
    # Check if we need more topics (trigger at 500 instead of 50)
    if len(existing_topics) < 500:
        print(f"[topics] Low on topics! Generating 100 more...")
        
        new_topics = generate_new_topics(100)
        
        # Append to file
        with open(topics_file, 'a', encoding='utf-8') as f:
            for topic in new_topics:
                f.write(f"{topic}\n")
        
        print(f"[topics] Added {len(new_topics)} new French topics!")
        print(f"[topics] Total topics now: {len(existing_topics) + len(new_topics)}")
    else:
        print(f"[topics] Enough topics available ({len(existing_topics)})")

if __name__ == '__main__':
    check_and_update_topics()
