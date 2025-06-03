# synthetic_markdown_generator
Building the Markdown and Style Variation Generator.
---

## I. Project Structure (Directory Layout)

A good structure will keep things organized. Here's a suggestion:

```
synthetic_markdown_generator/
├── data/
│   ├── raw_wikidump/         # Raw wikidump files (or links to them)
│   ├── processed_text/
│   │   ├── en/               # Cleaned English text snippets (paragraphs, titles, etc.)
│   │   └── bn/               # Cleaned Bangla text snippets
│   ├── assets/
│   │   ├── fonts/            # Any custom/downloaded font files
│   │   ├── non_text_images/  # Images to be used for backgrounds or decoration
│   │   └── equations/        # (Optional) Pre-defined LaTeX equations if not fully random
│   └── config/
│       ├── style_options.yaml # Configuration for CSS properties, fonts, colors, etc.
│       └── markdown_elements.yaml # Config for probabilities/rules of MD elements
├── output/
│   ├── set_001/
│   │   ├── 00001.md
│   │   ├── 00001.png
│   │   ├── 00002.md
│   │   ├── 00002.png
│   │   └── ...
│   └── ...                   # Other sets if you run generation in batches
├── src/
│   ├── __init__.py
│   ├── text_provider.py      # Loads and provides text snippets
│   ├── markdown_generator.py # Generates random Markdown content
│   ├── css_generator.py      # Generates random CSS styles
│   ├── html_renderer.py      # Converts MD+CSS to HTML
│   ├── image_capturer.py     # Renders HTML and captures screenshot
│   ├── utils.py              # Helper functions (e.g., random choices)
│   └── main.py               # Orchestrates the whole process
├── scripts/
│   ├── preprocess_wikidump.py # Script to extract and clean text from wikidumps
│   └── download_assets.py     # Script to download fonts, images (optional)
├── venv/                     # Virtual environment
├── requirements.txt          # Python dependencies
└── README.md                 # Project description
```

## II. Work Plan: Step-by-Step Implementation

This plan breaks down the project into manageable phases.

**Phase 0: Setup & Preparation**

1. **Environment Setup:**

   * Create the project directory structure.
   * Set up a Python virtual environment (`python -m venv venv`, `source venv/bin/activate`).
   * Install initial dependencies:
     * A Markdown library: `markdown-it-py` (very extensible, supports GFM) or `Python-Markdown`.
     * A headless browser library: `playwright` (modern, good API) or `selenium`.
     * For Wikidump processing: `mwparserfromhell` and potentially `wikiextractor`.
     * YAML for config: `PyYAML`.
     * `requests` if downloading assets.
   * Initialize Git repository.
2. **Data Acquisition & Initial Processing (Manual/Scripted):**

   * **`scripts/preprocess_wikidump.py` - Part 1: Extraction**
     * Download small samples of English and Bangla Wikidumps.
     * Use `wikiextractor` (or a similar tool) to convert Wikitext to cleaner text/JSON.
     * Store these initial raw extracts in `data/raw_wikidump/`.

**Phase 1: Core Text & Markdown Generation**

3. **Text Snippet Provider (`src/text_provider.py`):**

   * **Script: `scripts/preprocess_wikidump.py` - Part 2: Cleaning & Segmentation**
     * Input: Output from `wikiextractor`.
     * Use `mwparserfromhell` to further parse and clean wikitext artifacts (templates, refs if not handled by extractor).
     * Segment text into:
       * Headings (extract text from `== Title ==`).
       * Paragraphs.
       * List items (if easily identifiable).
       * Short phrases (for table cells, link texts).
     * Save cleaned, segmented text into `data/processed_text/en/` and `data/processed_text/bn/` (e.g., as `.txt` files or a simple JSON structure).
   * **Module: `src/text_provider.py`**
     * Functions to randomly load/select:
       * `get_random_paragraph(lang='en', min_sentences=1, max_sentences=5)`
       * `get_random_heading_text(lang='en')`
       * `get_random_phrase(lang='en', min_words=1, max_words=5)`
       * `get_random_word(lang='en')`
4. **Basic Markdown Generator (`src/markdown_generator.py`):**

   * Start with simple elements:
     * `generate_heading(level, text_provider)`
     * `generate_paragraph(text_provider)`
     * `generate_bold_italic_text(text_provider)` (wrapping words from `get_random_phrase`)
   * A main function `generate_markdown_document(text_provider, element_probabilities)`:
     * Randomly selects a sequence of elements to generate.
     * Uses `text_provider` to get content for these elements.
     * Concatenates them into a Markdown string.

**Phase 2: HTML Rendering and Image Capture**

5. **HTML Renderer (`src/html_renderer.py`):**

   * Input: Markdown string, CSS string (initially empty or very basic).
   * Use `markdown-it-py` to convert Markdown to an HTML fragment.
   * Wrap the fragment in a basic HTML document structure (`<html><head><style>...</style></head><body>...</body></html>`).
   * Inject the CSS string into the `<style>` tag.
   * Output: Full HTML string.
6. **Image Capturer (`src/image_capturer.py`):**

   * Input: HTML string.
   * Use `playwright` (recommended):
     * Launch a browser (Chromium, Firefox, WebKit).
     * Create a new page.
     * Set page content: `page.set_content(html_string)`.
     * Set viewport size (this will be a variation later): `page.set_viewport_size({"width": 800, "height": 600})`.
     * Take a screenshot: `page.screenshot(path="output.png")`.
     * Close browser.
   * Output: Saves an image file.
7. **Initial Orchestration (`src/main.py`):**

   * Initialize `TextProvider`.
   * Call `markdown_generator.generate_markdown_document()`.
   * Call `html_renderer.render_to_html()` (with placeholder CSS for now).
   * Call `image_capturer.capture_screenshot()`.
   * Save the `.md` and `.png` file.
   * *Goal: Get one simple Markdown file rendered to an image successfully.*

**Phase 3: CSS Generation and Styling Variations**

8. **Configuration for Styles (`data/config/style_options.yaml`):**

   * Define lists of options for CSS properties:
     * `fonts_en: ['Arial', 'Times New Roman', 'Verdana', 'Open Sans']`
     * `fonts_bn: ['SolaimanLipi', 'Hind Siliguri', 'Noto Sans Bengali']` (ensure these are installed or use web fonts)
     * `colors_text: ['#333333', '#000000', '#555555']`
     * `colors_background: ['#FFFFFF', '#F0F0F0', '#EFEFEF']`
     * `font_sizes_paragraph: [12px, 14px, 16pt]`
     * `font_sizes_h1: [2em, 2.5rem, 32px]`
     * Layout options (probabilities or choices for columns, alignments etc.)
   * This file will grow significantly.
9. **CSS Generator (`src/css_generator.py`):**

   * Load `style_options.yaml`.
   * Functions to generate CSS rules:
     * `generate_global_styles(config)`: Body background, default font, text color.
     * `generate_element_style(element_selector, config, element_type)`: e.g., `h1`, `p`, `table`.
       * Randomly pick font family, size, color, weight, etc., from config.
       * Randomly pick margin, padding.
     * `generate_layout_styles(config)`: Multi-column, content width/alignment.
   * A main function `generate_stylesheet(markdown_elements_present, config)`:
     * Generates global styles.
     * For each type of element present in the Markdown, generate specific styles.
     * Combine into a single CSS string.
10. **Integrate CSS into `main.py`:**

    * Call `css_generator.generate_stylesheet()` after generating Markdown.
    * Pass the generated CSS to `html_renderer.render_to_html()`.
    * *Goal: Generate images with basic randomized styling (fonts, colors).*

**Phase 4: Expanding Markdown & CSS Complexity**

11. **Expand `markdown_generator.py`:**

    * Implement functions for more complex elements:
      * `generate_list(ordered=True/False, depth=1, text_provider)`
      * `generate_table(rows, cols, text_provider)` (cells can have bold/italic)
      * `generate_blockquote(text_provider)`
      * `generate_code_block(lang_options, text_provider)` (use dummy code or snippets)
      * `generate_link(text_provider)`
      * `generate_image(image_path_provider)` (using images from `data/assets/non_text_images/`)
      * `generate_equation(text_provider)` (inline and block, use LaTeX snippets)
    * Improve `generate_markdown_document` to include these with varying probabilities.
    * Consider nesting rules (e.g., lists in blockquotes).
12. **Expand `css_generator.py`:**

    * Add styling options in `style_options.yaml` for all new Markdown elements.
    * Implement CSS generation for:
      * Table borders, cell padding, striping.
      * List markers, indentation.
      * Code block backgrounds, syntax highlighting themes (can be simple color changes).
      * Image floats, borders, shadows.
      * Header positioning (e.g., `text-align: center` for headers, specific margins).
      * Multi-column text (`column-count`, `column-gap`).
      * Text alignment (`text-align: justify/center/right`).
      * Background images for body or sections.
      * Varied viewport sizes in `image_capturer.py` (pass as parameter).
13. **Non-Text Images & Assets:**

    * **`scripts/download_assets.py` (Optional):** Script to download sample fonts (Google Fonts) and placeholder images (e.g., from Unsplash, Pexels via API, or a local collection). Store them in `data/assets/`.
    * Update `text_provider.py` or create an `asset_provider.py` to serve paths to these images and fonts.
    * Ensure fonts are correctly referenced in CSS (either system-installed or via `@font-face` if you self-host them or use web font URLs).

**Phase 5: Advanced Features, Bangla Support, and Refinement**

14. **Bangla Language Specifics:**

    * **Fonts:** Crucial. Ensure `style_options.yaml` has good Bangla fonts and `css_generator.py` uses them when `lang='bn'`.
    * **Text Direction:** For a small percentage of documents, set `body { direction: rtl; }` in CSS, even for Bangla (which is LTR script but sometimes documents are RTL formatted, or for comparison).
    * **Character Encoding:** Ensure all file I/O is UTF-8. Python 3 handles this well by default, but be mindful.
    * **Text Segmentation:** `text_provider.py` should handle Bangla text correctly.
15. **Complex Layouts & Styling:**

    * `css_generator.py`:
      * Header in the middle: Use `position: absolute` or flexbox/grid tricks for a specific "header-like" div you might inject into the HTML structure for this purpose.
      * More sophisticated `z-index` usage for overlapping elements.
      * CSS filters, blend modes (sparingly, for variety).
16. **Equations:**

    * If using LaTeX:
      * Include MathJax or KaTeX CDN link in the HTML template in `html_renderer.py`.
      * `markdown-it-py` might need a plugin like `markdown-it-mathjax` or you can manually wrap LaTeX in `$` or `$$`.
      * The `image_capturer.py` might need to wait for MathJax/KaTeX to render before taking a screenshot (e.g., `page.wait_for_function('typeof MathJax !== "undefined" && MathJax.typesetPromise')`).
17. **Error Handling & Logging:**

    * Implement robust error handling in `image_capturer.py` (e.g., if rendering fails).
    * Add logging throughout the process (how many files generated, any errors).
18. **Configuration for Generation (`data/config/markdown_elements.yaml`):**

    * Define probabilities for including each Markdown element.
    * Define ranges for counts (e.g., 1-3 paragraphs, then 0-1 tables).
    * Define nesting depths.
    * `main.py` will use this to drive `markdown_generator.py`.

**Phase 6: Scaling and Output Management**

19. **Batch Generation in `main.py`:**

    * Loop to generate N pairs of (Markdown, Image).
    * Organize output into subdirectories (`output/set_XXX/`) for manageability.
    * Use unique, sequential filenames.
20. **Performance Considerations:**

    * Headless browser operations are the slowest part.
    * Consider reusing browser instances if generating many images in one run (Playwright handles this well).
    * If Wikidump processing is slow, do it once and cache the `data/processed_text/`.
21. **Review and Iterate:**

    * Generate a small batch of images/Markdown.
    * Review them: Are the variations good? Is anything broken? Is the text readable (or intentionally unreadable for specific tests)?
    * Refine `style_options.yaml` and generation logic based on observations.

## III. Key Scripts and Their Interactions:

* **`scripts/preprocess_wikidump.py`**: One-time or infrequent run. Populates `data/processed_text/`.
* **`src/main.py` (Orchestrator)**:
  1. Initializes `TextProvider(config)`, `MarkdownGenerator(config, text_provider)`, `CssGenerator(config)`, `HtmlRenderer(markdown_lib)`, `ImageCapturer(browser_lib)`.
  2. In a loop (for N desired outputs):
     a.  `lang = random.choice(['en', 'bn'])`
     b.  `text_content_source = text_provider.get_text_for_document(lang)` (hypothetical function that gathers relevant text)
     c.  `markdown_string, present_elements = markdown_generator.generate_document(text_content_source, lang)`
     d.  `css_string = css_generator.generate_stylesheet(present_elements, lang)`
     e.  `html_string = html_renderer.render_to_html(markdown_string, css_string)`
     f.  `image_path, md_path = image_capturer.capture(html_string, output_dir, base_filename)`
     g.  Save `markdown_string` to `md_path`.
     h.  Log progress.

This detailed plan should give you a solid roadmap. Remember to start simple, get one part working, and then gradually add complexity. Version control (Git) will be your best friend!

