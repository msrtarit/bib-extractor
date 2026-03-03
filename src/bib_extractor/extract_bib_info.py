import os
import re
import json
import argparse
from pathlib import Path
from pypdf import PdfReader

def get_num(s: str) -> int:
    """Extract leading number from filename for sorting."""
    m = re.match(r"(\d+)", s)
    return int(m.group(1)) if m else 999

def extract_papers(dir_path: Path) -> list:
    """Iterate over PDF files, extract DOI or title, and return list of dicts."""
    files = [f for f in os.listdir(dir_path) if f.lower().endswith('.pdf')]
    files.sort(key=get_num)
    doi_pattern = re.compile(r"10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+")
    results = []
    for filename in files:
        full_path = dir_path / filename
        print(f"Processing {filename}...")
        try:
            # Extract first two pages as text using pypdf
            reader = PdfReader(str(full_path))
            content = ""
            # Read at most the first 2 pages
            for i in range(min(2, len(reader.pages))):
                content += reader.pages[i].extract_text() + "\n"
                
            dois = doi_pattern.findall(content)
            if dois:
                doi = max(dois, key=len)
                results.append({'file': filename, 'doi': doi})
                print(f"  Found DOI: {doi}")
            else:
                # Fallback: use first few non‑empty lines as title candidate
                lines = [l.strip() for l in content.split('\n') if l.strip()]
                title = " ".join(lines[:3]) if lines else "Unknown"
                results.append({'file': filename, 'title': title})
                print(f"  No DOI found. Title candidate: {title[:50]}...")
        except Exception as e:
            results.append({'file': filename, 'error': str(e)})
            print(f"  Error: {e}")
    return results

def main():
    parser = argparse.ArgumentParser(
        description='Extract DOIs or titles from PDF papers in a folder.'
    )
    parser.add_argument(
        '--dir',
        type=Path,
        default=Path.cwd(),
        help='Directory containing PDF files (default: current working directory)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('paper_info.json'),
        help='Path to write the JSON output (default: paper_info.json)'
    )
    args = parser.parse_args()
    results = extract_papers(args.dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Done! Saved results to {args.output}")

if __name__ == '__main__':
    main()
