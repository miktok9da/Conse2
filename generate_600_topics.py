"""
Generate 600 French topics about ancient women's history.
"""

import requests
from urllib.parse import quote
from pathlib import Path
import time

def generate_french_topics_batch(batch_num, count=100):
    """Generate a batch of French topics."""
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("POLLINATIONS_API_KEY")
    base_url = "https://gen.pollinations.ai/text/"
    
    # Simpler system prompt
    system = (
        "You are a historian specialized in ancient women's history. "
        f"Create {count} unique topics in French about women in ancient civilizations. "
        "Each topic should be 5-10 words, interesting and educational. "
        "Cover: laws, customs, famous women, professions, religion, culture, art. "
        "Output ONLY the topics, one per line, no numbers or bullets."
    )
    
    prompt = f"Generate {count} unique French topics about women in ancient civilizations"
    
    url = base_url + quote(prompt)
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    params = {"model": "openai", "temperature": 0.9, "system": system}
    
    print(f"[batch {batch_num}] Generating {count} French topics...")
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=120)
        r.raise_for_status()
        
        # Parse topics
        topics = []
        for line in r.text.strip().split('\n'):
            cleaned = line.strip()
            # Remove common prefixes
            for prefix in ['- ', '* ', '• ', '→ ', '> ']:
                if cleaned.startswith(prefix):
                    cleaned = cleaned[len(prefix):]
            # Remove numbering
            import re
            cleaned = re.sub(r'^\d+[\.\:\)\-]\s*', '', cleaned)
            
            if cleaned and len(cleaned) > 5:
                topics.append(cleaned)
        
        print(f"[batch {batch_num}] Generated {len(topics)} topics")
        return topics[:count]
    
    except Exception as e:
        print(f"[batch {batch_num}] Error: {e}")
        return []

def main():
    """Generate 600 French topics in batches."""
    
    all_topics = []
    batches = 6  # 6 batches of 100 = 600 topics
    
    for i in range(batches):
        topics = generate_french_topics_batch(i+1, 100)
        all_topics.extend(topics)
        
        print(f"[progress] Total topics so far: {len(all_topics)}")
        
        # Wait between batches to avoid rate limits
        if i < batches - 1:
            print("[progress] Waiting 5 seconds before next batch...")
            time.sleep(5)
    
    # Write to file
    topics_file = Path('topics.txt')
    with open(topics_file, 'w', encoding='utf-8') as f:
        for topic in all_topics:
            f.write(f"{topic}\n")
    
    print(f"\n[done] Generated {len(all_topics)} French topics!")
    print(f"[done] Saved to {topics_file}")

if __name__ == '__main__':
    main()
