import os
import json
import random

class TextProvider:
    def __init__(self, lang='en'):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        seg_dir = os.path.join(base_dir, f"data/processed_text/{lang}/segments")
        self.data = {}
        for key in ['headings', 'paragraphs', 'lists', 'phrases', 'words']:
            with open(os.path.join(seg_dir, f"{key}.json"), encoding="utf-8") as f:
                self.data[key] = json.load(f)

    def get_random_paragraph(self, min_sentences=1, max_sentences=5):
        para = random.choice(self.data['paragraphs'])
        sentences = [s.strip() for s in para.split('.') if s.strip()]
        n = random.randint(min_sentences, min(max_sentences, len(sentences)))
        return '. '.join(sentences[:n]) + '.'

    def get_random_heading_text(self):
        return random.choice(self.data['headings'])

    def get_random_phrase(self, min_words=1, max_words=5):
        phrase = random.choice(self.data['phrases'])
        words = phrase.split()
        n = random.randint(min_words, min(max_words, len(words)))
        return ' '.join(words[:n])

    def get_random_word(self):
        return random.choice(self.data['words'])