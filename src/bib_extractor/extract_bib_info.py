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
    
    # Robust DOI pattern: 
    # 1. Matches "10."
    # 2. Allows any combination of digits and spaces for the prefix (to handle "1 109")
    # 3. Matches "/"
    # 4. Matches the suffix, allowing internal periods/dashes but stopping at typical non-DOI boundaries
    # We will clean the result after matching.
    doi_pattern = re.compile(r"10\.\s*[0-9\s]{4,15}/\s*[a-zA-Z0-9._\-/()]+")
    
    results = []
    for filename in files:
        full_path = dir_path / filename
        print(f"Processing {filename}...")
        try:
            reader = PdfReader(str(full_path))
            content = ""
            for i in range(min(2, len(reader.pages))):
                content += reader.pages[i].extract_text() + "\n"
                
            match = doi_pattern.search(content)
            if match:
                # Clean: remove ALL whitespace from the match
                doi = re.sub(r"\s+", "", match.group(0))
                # Discard trailing dots or punctuation
                doi = re.sub(r"[^a-zA-Z0-9)]+$", "", doi)
                
                results.append({'file': filename, 'doi': doi})
                print(f"  Found DOI: {doi}")
            else:
                # Secondary attempt: strip ONLY newlines and search again
                # Sometimes a DOI is split by a newline
                flat_content = content.replace("\n", " ").replace("\r", " ")
                match = doi_pattern.search(flat_content)
                if match:
                    doi = re.sub(r"\s+", "", match.group(0))
                    doi = re.sub(r"[^a-zA-Z0-9)]+$", "", doi)
                    results.append({'file': filename, 'doi': doi})
                    print(f"  Found DOI (post-clean): {doi}")
                else:
                    # Fallback: title extraction
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
