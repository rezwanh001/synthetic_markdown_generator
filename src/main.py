# src/main.py

import os
import random
import argparse
from text_provider import TextProvider
from markdown_generator import MarkdownGenerator
from html_renderer import render_to_html
from image_capturer import capture_screenshot

def main(args):
    print("Starting synthetic document generation...")
    print(f"Language mode: {args.lang}")
    print(f"Number of files to generate: {args.num_files}")

    # --- Configuration ---
    # Use the language argument passed from the command line
    lang = args.lang 
    
    # --- CHANGE: Make the output directory name dynamic based on the language ---
    output_dir = f"output/{lang}_set_001"
    
    print(f"Output will be saved in: {output_dir}")

    element_probabilities = {
        'heading': 0.15,
        'paragraph': 0.50,
        'bold_italic': 0.20,
        'list': 0.15,
    }
    
    # --- Setup ---
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize our generator components with the chosen language
    text_provider = TextProvider(lang=lang)
    markdown_generator = MarkdownGenerator(text_provider)
    
    # --- Generation Loop ---
    # Use the number of files argument from the command line
    for i in range(1, args.num_files + 1):
        filename_base = f"{i:05d}"
        md_path = os.path.join(output_dir, f"{filename_base}.md")
        png_path = os.path.join(output_dir, f"{filename_base}.png")
        
        print(f"Generating {filename_base}...")

        # 1. Generate Markdown content
        num_elements = random.randint(5, 15) 
        markdown_content = markdown_generator.generate_document(
            num_elements=num_elements,
            element_probabilities=element_probabilities
        )
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        # 2. Generate CSS (for now, a placeholder)
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
        """
        
        # 3. Render Markdown+CSS to HTML
        html_content = render_to_html(markdown_content, css_content)

        # 4. Capture screenshot of the rendered HTML
        capture_screenshot(html_content, png_path)
        
        print(f"  -> Saved: {md_path} and {png_path}")

    print("\nGeneration complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic Markdown documents.")
    
    parser.add_argument(
        '--lang', 
        type=str, 
        default='en', 
        choices=['en', 'bn', 'both'],
        help="Language to use for text generation: 'en' for English, 'bn' for Bengali, 'both' for mixed."
    )
    
    parser.add_argument(
        '-n', '--num-files',
        type=int,
        default=5,
        help="Number of document pairs (md/png) to generate."
    )

    parsed_args = parser.parse_args()
    main(parsed_args)