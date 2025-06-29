# src/markdown_generator.py

import random
from text_provider import TextProvider

class MarkdownGenerator:
    """
    Generates a complete Markdown document with a random structure and content.
    """
    def __init__(self, text_provider: TextProvider):
        """
        Initializes the generator with a text provider.
        
        Args:
            text_provider: An instance of TextProvider to get text snippets from.
        """
        self.tp = text_provider
        
        # This dictionary maps the element name to its generation function.
        # This makes it easy to add new elements later.
        # self._element_generators = {
        #     'heading': self._generate_heading,
        #     'paragraph': self._generate_paragraph,
        #     'bold_italic': self._generate_bold_italic,
        #     # We will add more here later, e.g., 'list', 'table', 'code_block'
        # }

        self._element_generators = {
            'heading': self._generate_heading,
            'paragraph': self._generate_paragraph,
            'bold_italic': self._generate_bold_italic,
            'list': self._generate_list, # Add this line
        }

    # --- Private methods for generating individual Markdown elements ---

    def _generate_heading(self):
        """Generates a random heading (H2-H4)."""
        level = random.randint(2, 4)  # Let's stick to H2-H4 for typical content
        text = self.tp.get_random_heading_text()
        return f"{'#' * level} {text}\n\n"

    def _generate_paragraph(self):
        """Generates a random paragraph."""
        text = self.tp.get_random_paragraph()
        return f"{text}\n\n"
        
    def _generate_bold_italic(self):
        """
        Generates a paragraph containing a random bolded or italicized phrase.
        This is a more realistic way to use inline formatting.
        """
        paragraph = self.tp.get_random_paragraph()
        words = paragraph.split()
        
        if len(words) < 5: # If the paragraph is too short, just return it
            return f"{paragraph}\n\n"

        # Select a random phrase to format
        start_index = random.randint(0, len(words) - 3)
        end_index = start_index + random.randint(2, 4)
        phrase_to_format = " ".join(words[start_index:end_index])

        # Choose a random format
        style = random.choice(['**', '*', '***']) # bold, italic, bold+italic
        
        formatted_phrase = f"{style}{phrase_to_format}{style}"
        
        # Replace the original phrase with the formatted one
        # Using the count=1 ensures we only replace the first occurrence
        new_paragraph = paragraph.replace(phrase_to_format, formatted_phrase, 1)
        
        return f"{new_paragraph}\n\n"

    def _generate_list(self):
        """Generates a random ordered or unordered list."""
        list_type = random.choice(['* ', '1. ']) # Unordered or Ordered
        num_items = random.randint(3, 7)
        
        items = []
        for _ in range(num_items):
            # Use our new TextProvider method!
            item_text = self.tp.get_random_list_item()
            items.append(f"{list_type}{item_text}")
            
        return "\n".join(items) + "\n\n"


    # --- Public method to generate the full document ---

    def generate_document(self, num_elements: int, element_probabilities: dict):
        """
        Generates a full Markdown document string.

        Args:
            num_elements: The total number of elements to generate in the document.
            element_probabilities: A dictionary mapping element names to their
                                   probability (e.g., {'heading': 0.2, 'paragraph': 0.8}).

        Returns:
            A string containing the full Markdown document.
        """
        
        # Get the list of possible elements and their corresponding weights
        element_names = list(element_probabilities.keys())
        element_weights = list(element_probabilities.values())
        
        markdown_parts = []
        
        # Always start with a H1 title
        markdown_parts.append(f"# {self.tp.get_random_heading_text()}\n\n")

        for _ in range(num_elements):
            # Choose an element type based on the probabilities
            # `random.choices` returns a list, so we take the first item
            chosen_element_name = random.choices(element_names, weights=element_weights, k=1)[0]
            
            # Get the generator function for that element
            generator_func = self._element_generators[chosen_element_name]
            
            # Call the function and add its output to our list
            markdown_parts.append(generator_func())
            
        return "".join(markdown_parts)