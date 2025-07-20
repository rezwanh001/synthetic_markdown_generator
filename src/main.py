# src/main.py

import os
import random
import argparse
from text_provider import TextProvider
from markdown_generator import MarkdownGenerator
from html_renderer import render_to_html
# Updated import to reflect the new function name
from image_capturer import render_and_capture

def main(args):
    print("Starting synthetic document generation...")
    print(f"Language mode: {args.lang}")
    print(f"Number of files to generate: {args.num_files}")
    if args.pdf:
        print("PDF generation: ENABLED")

    lang = args.lang 
    output_dir = f"output/{lang}_set_001"
    print(f"Output will be saved in: {output_dir}")

    element_probabilities = {
        'heading': 0.15,
        'paragraph': 0.50,
        'bold_italic': 0.20,
        'list': 0.15,
    }
    
    os.makedirs(output_dir, exist_ok=True)
    
    text_provider = TextProvider(lang=lang)
    markdown_generator = MarkdownGenerator(text_provider)
    
    for i in range(1, args.num_files + 1):
        filename_base = f"{i:05d}"
        md_path = os.path.join(output_dir, f"{filename_base}.md")
        png_path = os.path.join(output_dir, f"{filename_base}.png")
        # Define the PDF path as well
        pdf_path = os.path.join(output_dir, f"{filename_base}.pdf")
        
        print(f"Generating {filename_base}...")

        num_elements = random.randint(10, 25) # Increased elements to test long documents
        markdown_content = markdown_generator.generate_document(
            num_elements=num_elements,
            element_probabilities=element_probabilities
        )
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        css_content = """
            body { 
                font-family: 'Times New Roman', 'SolaimanLipi', serif; 
                margin: 40px; 
                max-width: 800px; 
            }
            h1, h2, h3, h4 { 
                font-family: 'Arial', 'Hind Siliguri', sans-serif;
                color: #333; 
                border-bottom: 1px solid #ccc; 
                padding-bottom: 5px;
            }
            p { line-height: 1.6; }
            /* Ensure list styles are visible */
            ul, ol { padding-left: 40px; }
        """
        
        html_content = render_to_html(markdown_content, css_content)

        # Use the new, more powerful capture function
        render_and_capture(
            html_string=html_content,
            png_path=png_path,
            # Pass the pdf_path only if the --pdf flag was used
            pdf_path=pdf_path if args.pdf else None
        )
        
        saved_files = f"{md_path} and {png_path}"
        if args.pdf:
            saved_files += f" and {pdf_path}"
        print(f"  -> Saved: {saved_files}")

    print("\nGeneration complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic Markdown documents.")
    
    parser.add_argument(
        '--lang', 
        type=str, 
        default='en', 
        choices=['en', 'bn', 'both'],
        help="Language to use for text generation."
    )
    
    parser.add_argument(
        '-n', '--num-files',
        type=int,
        default=5,
        help="Number of document pairs to generate."
    )
    
    # --- ADDED: New argument for PDF generation ---
    parser.add_argument(
        '--pdf',
        action='store_true', # This makes it a flag, e.g., --pdf
        help="Enable PDF generation in addition to PNG images."
    )

    parsed_args = parser.parse_args()
    main(parsed_args)