import os
import json
import glob
import mwparserfromhell
from tqdm import tqdm

def clean_and_segment(lang):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_dir, f"data/processed_text/{lang}")
    output_dir = os.path.join(base_dir, f"data/processed_text/{lang}/segments")
    os.makedirs(output_dir, exist_ok=True)

    headings, paragraphs, lists, phrases, words = [], [], [], [], []

    wiki_files = glob.glob(f"{input_dir}/**/wiki_*", recursive=True)
    for wiki_file in tqdm(wiki_files, desc=f"Processing {lang} Wikipedia"):
        with open(wiki_file, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                try:
                    article = json.loads(line.strip())
                    text = article.get('text', '')
                    if not text.strip():
                        continue

                    # Headings using mwparserfromhell
                    wikicode = mwparserfromhell.parse(text)
                    for heading in wikicode.filter_headings():
                        h = heading.title.strip_code().strip()
                        if h:
                            headings.append(h)

                    # Paragraphs, lists, phrases, words (line-based)
                    for l in text.split('\n'):
                        l = l.strip()
                        if not l:
                            continue
                        # List items (wikitext: *, #, - at the start)
                        if l.startswith(('*', '#', '-')):
                            lists.append(l.lstrip('*#- ').strip())
                        else:
                            paragraphs.append(l)
                            # Short phrases (max 5 words)
                            for phrase in l.replace('।', '.').split('.'):
                                phrase = phrase.strip()
                                if 1 <= len(phrase.split()) <= 5:
                                    phrases.append(phrase)
                            words.extend([w for w in l.split() if w])
                except Exception as e:
                    if idx < 3:
                        print(f"Error parsing line {idx}: {e}")
                    continue

    print(f"Extracted: {len(headings)} headings, {len(paragraphs)} paragraphs, {len(lists)} lists, {len(phrases)} phrases, {len(words)} words.")

    # Save as JSON
    with open(os.path.join(output_dir, "headings.json"), "w", encoding="utf-8") as f:
        json.dump(headings, f, ensure_ascii=False)
    with open(os.path.join(output_dir, "paragraphs.json"), "w", encoding="utf-8") as f:
        json.dump(paragraphs, f, ensure_ascii=False)
    with open(os.path.join(output_dir, "lists.json"), "w", encoding="utf-8") as f:
        json.dump(lists, f, ensure_ascii=False)
    with open(os.path.join(output_dir, "phrases.json"), "w", encoding="utf-8") as f:
        json.dump(phrases, f, ensure_ascii=False)
    with open(os.path.join(output_dir, "words.json"), "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False)

def main():
    for lang in ['en', 'bn']:
        print(f"Segmenting and cleaning {lang} Wikipedia...")
        clean_and_segment(lang)
        print(f"Done for {lang}.")

if __name__ == "__main__": 
    main()