import subprocess
import os
import json
import glob

def extract_wikidump(lang):
    """Extract text from Wikipedia dump using wikiextractor."""
    dump_file = f"data/raw_wikidump/{lang}wiki-latest-pages-articles.xml.bz2"
    output_dir = f"data/processed_text/{lang}"
    os.makedirs(output_dir, exist_ok=True)
    # Run wikiextractor with JSON output
    subprocess.run([
        "python", "scripts/wikiextractor/wikiextractor.py",
        dump_file, "-o", output_dir, "--json"
    ], check=True)

def process_extracted_text(lang):
    """Process extracted JSON files into text snippets."""
    output_dir = f"data/processed_text/{lang}"
    # wikiextractor outputs files in subdirectories (e.g., AA/wiki_00)
    wiki_files = glob.glob(f"{output_dir}/**/wiki_*", recursive=True)
    snippets = []
    for wiki_file in wiki_files:
        with open(wiki_file, 'r', encoding='utf-8') as f:
            for line in f:
                article = json.loads(line.strip())
                text = article.get('text', '')
                # Split into paragraphs
                paragraphs = text.split('\n\n')
                snippets.extend([p.strip() for p in paragraphs if p.strip()])
    # Save snippets as individual files
    os.makedirs(f"{output_dir}/snippets", exist_ok=True)
    for i, snippet in enumerate(snippets):
        with open(f"{output_dir}/snippets/snippet_{i}.txt", 'w', encoding='utf-8') as f:
            f.write(snippet)

def main():
    languages = ['en', 'bn']
    for lang in languages:
        print(f"Processing {lang} Wikipedia dump...")
        extract_wikidump(lang)
        process_extracted_text(lang)
        print(f"Completed processing for {lang}.")

if __name__ == "__main__":
    main()