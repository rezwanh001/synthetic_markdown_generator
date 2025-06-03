import requests
import os

def download_file(url, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"Downloaded: {local_filename}")

def main():
    dumps = {
        "en": "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2",
        "bn": "https://dumps.wikimedia.org/bnwiki/latest/bnwiki-latest-pages-articles.xml.bz2"
    }
    dest_folder = "data/raw_wikidump"
    for lang, url in dumps.items():
        print(f"Downloading {lang} Wikipedia dump...")
        download_file(url, dest_folder)

if __name__ == "__main__":
    main()