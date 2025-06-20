import os
from text_provider import TextProvider
from markdown_generator import generate_markdown_document
from html_renderer import render_to_html
from image_capturer import capture_screenshot

def main():
    # Output paths
    output_dir = "output/set_001"
    os.makedirs(output_dir, exist_ok=True)
    md_path = os.path.join(output_dir, "00001.md")
    png_path = os.path.join(output_dir, "00001.png")

    # 1. Text provider
    tp = TextProvider(lang='en')

    # 2. Generate markdown
    element_probs = {'heading': 0.2, 'paragraph': 0.6, 'bold_italic': 0.2}
    md = generate_markdown_document(tp, element_probs, num_elements=10)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    # 3. Render HTML
    css = "body { font-family: Arial, sans-serif; font-size: 18px; }"
    html = render_to_html(md, css)

    # 4. Capture screenshot
    capture_screenshot(html, png_path)
    print(f"Saved: {md_path}, {png_path}")

if __name__ == "__main__":
    main()