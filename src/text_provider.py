# src/text_provider.py

import os
import json
import random

class TextProvider:
    def __init__(self, lang='en'):
        """
        Initializes the TextProvider.

        Args:
            lang (str): Can be 'en', 'bn', or 'both'.
                        If 'both', it loads data for both languages.
        """
        print(f"Initializing TextProvider for language mode: '{lang}'")
        self.langs_to_load = []
        self.data = {}

        # This is the key logic: determine which language folders to read from.
        if lang == 'both':
            self.langs_to_load = ['en', 'bn']
        else:
            self.langs_to_load = [lang]

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Loop over the languages we need to load ('en', 'bn', or just one of them)
        for l in self.langs_to_load:
            print(f"  -> Loading data for '{l}'...")
            self.data[l] = {}
            # This constructs the correct path to the 'en' and 'bn' folders
            seg_dir = os.path.join(base_dir, f"data/processed_text/{l}/segments")
            for key in ['headings', 'paragraphs', 'phrases', 'words']:
                filepath = os.path.join(seg_dir, f"{key}.json")
                try:
                    with open(filepath, encoding="utf-8") as f:
                        self.data[l][key] = json.load(f)
                except FileNotFoundError:
                    print(f"   [Warning] Data file not found at {filepath}.")
                    self.data[l][key] = []

            if not self.data[l]['paragraphs'] or not self.data[l]['headings']:
                raise Exception(f"Essential data files for lang '{l}' are missing or empty in {seg_dir}. Please run the preprocessing script again.")

    def _get_random_data(self, key):
        """Internal helper to get a random piece of data from a random language."""
        # Choose a language at random from the loaded languages
        chosen_lang = random.choice(self.langs_to_load)
        
        data_list = self.data[chosen_lang].get(key, [])
        
        if not data_list:
            # Fallback to the other language if the chosen one's data is empty
            for l in self.langs_to_load:
                if l != chosen_lang:
                    fallback_list = self.data[l].get(key, [])
                    if fallback_list:
                        return random.choice(fallback_list)
            return f"default {key[:-1]}"
            
        return random.choice(data_list)

    def get_random_paragraph(self, min_sentences=1, max_sentences=3):
        para = self._get_random_data('paragraphs')
        sentences = [s.strip() for s in para.replace('।', '.').split('.') if s.strip()]
        if not sentences: return para

        num_to_take = random.randint(min_sentences, min(max_sentences, len(sentences)))
        return '. '.join(sentences[:num_to_take]) + '.'

    def get_random_heading_text(self):
        return self._get_random_data('headings')

    def get_random_phrase(self, min_words=2, max_words=8):
        attempts = 0
        while attempts < 100:
            phrase = self._get_random_data('phrases')
            words = phrase.split()
            
            if len(words) >= min_words:
                num_to_take = random.randint(min_words, min(max_words, len(words)))
                return ' '.join(words[:num_to_take])
            
            attempts += 1
            
        # Fallback if no suitable phrase is found
        phrase = self._get_random_data('phrases')
        return phrase if phrase else "default phrase fallback"

    def get_random_word(self):
        return self._get_random_data('words')

    def get_random_list_item(self):
        return self.get_random_phrase(min_words=2, max_words=10)