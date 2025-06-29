# scripts/preprocess_wikidump.py

import os
import json
import re
import glob
import mwparserfromhell
from tqdm import tqdm

def clean_and_segment(lang):
    MAX_ARTICLES_TO_PROCESS = 10000 
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, f"data/processed_text/{lang}")
    output_dir = os.path.join(base_dir, f"data/processed_text/{lang}/segments")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(input_dir) or not os.listdir(input_dir):
        print(f"ERROR: Input directory not found or is empty: {input_dir}")
        print("Please run wikiextractor first.")
        return

    # --- CHANGE 1: Use a 'set' for words to automatically handle uniqueness and save memory ---
    headings, paragraphs, lists, phrases, words = [], [], [], [], set()
    
    processed_articles = 0
    stop_processing = False

    wiki_files = glob.glob(f"{input_dir}/**/wiki_*", recursive=True)
    
    for wiki_file in tqdm(wiki_files, desc=f"Processing files for '{lang}'"):
        if stop_processing:
            break
            
        with open(wiki_file, 'r', encoding='utf-8') as f:
            for line in f:
                if processed_articles >= MAX_ARTICLES_TO_PROCESS:
                    stop_processing = True
                    break

                try:
                    article = json.loads(line.strip())
                    text = article.get('text', '')
                    title = article.get('title', '')
                    if not text.strip() or not title.strip():
                        continue

                    # --- CHANGE 2: Improved Heading Extraction ---
                    # Use the article's main title as a guaranteed H1-level heading.
                    headings.append(title)
                    
                    # Also try to get section headings from the wikitext, but don't rely on it.
                    wikicode = mwparserfromhell.parse(text)
                    for heading in wikicode.filter_headings():
                        h_text = heading.title.strip_code().strip()
                        if h_text:
                            headings.append(h_text)
                    
                    clean_text = wikicode.strip_code().strip()
                    
                    # --- CHANGE 3: Improved Paragraph and List Segmentation ---
                    # Split by double newlines to get actual paragraphs, not just lines.
                    for block in clean_text.split('\n\n'):
                        block = block.strip()
                        if not block or block.startswith(('|', '{', '!', '}', '<')):
                            continue

                        # Check if the block is a list
                        if block.startswith(('*', '#', '-')):
                            # Split list items within the block
                            for item in block.split('\n'):
                                clean_item = item.lstrip('*#- ').strip()
                                if clean_item:
                                    lists.append(clean_item)
                        else:
                            # It's a paragraph
                            paragraphs.append(block)
                            
                            # Extract phrases and words from the paragraph
                            # Use regex to split by sentence-ending punctuation
                            for phrase in re.split(r'[.।!?]\s', block):
                                phrase = phrase.strip()
                                if 1 <= len(phrase.split()) <= 10:
                                    phrases.append(phrase)
                            
                            # Use .update() for sets, which is like extend() for lists
                            words.update([w.strip('.,!?;:"()[]') for w in block.split() if w.strip('.,!?;:"()[]')])

                except Exception:
                    continue
                
                processed_articles += 1

    print(f"\nFinished processing for {lang}. Extracted from {processed_articles} articles.")
    # The count for words will now be accurate because we used a set.
    print(f"Found: {len(headings)} headings, {len(paragraphs)} paragraphs, {len(lists)} lists, {len(phrases)} phrases, {len(words)} unique words.")

    # Save the collected data to JSON files
    with open(os.path.join(output_dir, "headings.json"), "w", encoding="utf-8") as f:
        json.dump(headings, f, ensure_ascii=False, indent=2)
    with open(os.path.join(output_dir, "paragraphs.json"), "w", encoding="utf-8") as f:
        json.dump(paragraphs, f, ensure_ascii=False, indent=2)
    with open(os.path.join(output_dir, "lists.json"), "w", encoding="utf-8") as f:
        json.dump(lists, f, ensure_ascii=False, indent=2)
    with open(os.path.join(output_dir, "phrases.json"), "w", encoding="utf-8") as f:
        json.dump(phrases, f, ensure_ascii=False, indent=2)
    # Convert the set to a list for JSON serialization
    with open(os.path.join(output_dir, "words.json"), "w", encoding="utf-8") as f:
        json.dump(list(words), f, ensure_ascii=False, indent=2)

def main():
    for lang in ['en', 'bn']:
        print(f"--- Starting segmentation for '{lang}' ---")
        clean_and_segment(lang)
        print(f"--- Done for '{lang}' ---\n")

if __name__ == "__main__": 
    main()