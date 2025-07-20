# Markdown Style Generator

## Overview
The Markdown Style Generator is a Python project designed to facilitate the generation of Markdown content with various style variations. This tool allows users to create structured Markdown documents easily and apply different styles to enhance the presentation of their content.

## Features
- Generate Markdown content programmatically.
- Apply various style variations to the generated Markdown.
- Modular design with separate components for Markdown generation and style management.

## Installation
To install the required dependencies, navigate to the project directory and run:

```
pip install -r requirements.txt
```

## Activate the environment:

```bash
source venv/bin/activate
```

## Change the directory:
```bash
cd synthetic_markdown_generator/
```

### To Download WiKidump (bn & en):
```bash
python scripts/download_wikidump.py
```

### To Preprocess WiKidump (bn & en) `MAX_ARTICLES_TO_PROCESS = 10000`:
```bash
python scripts/preprocess_wikidump.py
```

### Steps to Run `src/main.py`:
- 1. To generate 10 English-only documents:
```bash
python src/main.py --lang en --num-files 10
```

- 2. To generate 3 Bengali-only documents:
```bash
python src/main.py --lang bn -n 3
```

- 3. To generate 5 mixed-language documents (the new feature!):
```bash
python src/main.py --lang both
```

- 4. To see the help message for your script:
```bash
python src/main.py --help
```

- 5. Generate 3 mixed-language documents (MD and full-page PNG only) [New]
```bash
python src/main.py --lang both -n 3
```

- 6. Generate 3 mixed-language documents and ALSO generate a PDF for each: [New]
```bash
python src/main.py --lang both -n 3 --pdf
```


## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.



