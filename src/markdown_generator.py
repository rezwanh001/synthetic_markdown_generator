import random

def generate_heading(level, text_provider):
    text = text_provider.get_random_heading_text()
    return f"{'#' * level} {text}"

def generate_paragraph(text_provider):
    return text_provider.get_random_paragraph()

def generate_bold_italic_text(text_provider):
    phrase = text_provider.get_random_phrase()
    style = random.choice(['**', '*', '***'])
    return f"{style}{phrase}{style}"

def generate_markdown_document(text_provider, element_probabilities, num_elements=10):
    elements = []
    for _ in range(num_elements):
        element_type = random.choices(
            population=list(element_probabilities.keys()),
            weights=list(element_probabilities.values())
        )[0]
        if element_type == 'heading':
            elements.append(generate_heading(random.randint(1, 3), text_provider))
        elif element_type == 'paragraph':
            elements.append(generate_paragraph(text_provider))
        elif element_type == 'bold_italic':
            elements.append(generate_bold_italic_text(text_provider))
    return '\n\n'.join(elements)