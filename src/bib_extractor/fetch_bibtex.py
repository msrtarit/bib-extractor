import argparse
import json
import time
import urllib.request
import re
from pathlib import Path
from typing import List, Dict, Any

def load_papers(json_path: Path) -> List[Dict[str, Any]]:
    """Load the JSON file produced by ``extract_bib_info.py``."""
    if not json_path.is_file():
        raise FileNotFoundError(f"Input file not found: {json_path}")
    with json_path.open(encoding="utf-8") as f:
        return json.load(f)

def fetch_bibtex(doi: str, timeout: int = 10) -> str:
    """Retrieve a BibTeX entry for a DOI."""
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8")

def parse_bibtex(bib: str) -> Dict[str, str]:
    """Simple regex‑based parser to extract key fields from a BibTeX entry."""
    data = {}
    fields = ["title", "year", "author"]
    for field in fields:
        # Match field = {content} or field = "content"
        match = re.search(f"{field}\\s*=\\s*[\\{{\"](.*?)[\\}}\"]", bib, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Clean up author if multiple
            if field == "author" and " and " in content:
                content = content.split(" and ")[0]  # Take first author
            # Remove BibTeX escapes like \'{e} or {T}itanic
            content = re.sub(r"[\{\}]", "", content)
            data[field] = content
    return data

def sanitize_filename(filename: str) -> str:
    """Remove characters that are invalid in filenames."""
    return re.sub(r'[/\\:*?"<>|]', "", filename)

def rename_paper(old_path: Path, bib_data: Dict[str, str]) -> Path:
    """Rename a PDF file based on BibTeX data."""
    if not old_path.exists():
        return old_path

    year = bib_data.get("year", "UnknownYear")
    author = bib_data.get("author", "UnknownAuthor")
    title = bib_data.get("title", "UnknownTitle")
    
    # Format: Year - Author - Title.pdf (limit title length)
    new_name = f"{year} - {author} - {title[:60]}"
    new_name = sanitize_filename(new_name) + ".pdf"
    new_path = old_path.parent / new_name
    
    # Avoid overwriting or errors if name is same
    if old_path != new_path:
        # If destination exists, add a suffix
        counter = 1
        final_path = new_path
        while final_path.exists():
            final_path = new_path.with_name(f"{new_path.stem}_{counter}.pdf")
            counter += 1
        old_path.rename(final_path)
        return final_path
    return old_path

def write_bibtex(entries: List[str], output_path: Path) -> None:
    """Write a list of BibTeX entries to ``output_path``."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for entry in entries:
            f.write(entry.rstrip() + "\n\n")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch BibTeX entries for papers and optionally rename original PDFs."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("paper_info.json"),
        help="Path to the JSON file produced by extract_bib_info (default: paper_info.json).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("papers.bib"),
        help="Path to write the combined BibTeX file (default: papers.bib).",
    )
    parser.add_argument(
        "--rename",
        action="store_true",
        help="If set, rename the original PDF files using fetched metadata.",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        help="Directory containing the original PDFs (required if --rename is used).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Seconds to wait between requests (default: 1.0).",
    )
    args = parser.parse_args()

    if args.rename and not args.dir:
        print("[ERROR] You must provide --dir when using --rename.")
        return

    try:
        papers = load_papers(args.input)
    except Exception as exc:
        print(f"[ERROR] Could not read input file: {exc}")
        return

    bib_entries: List[str] = []
    for paper in papers:
        doi = paper.get("doi")
        if not doi:
            print(f"[SKIP] {paper.get('file', '<unknown>')}: no DOI present.")
            continue
            
        print(f"[FETCH] {paper.get('file', '<unknown>')} ({doi}) …")
        try:
            bib = fetch_bibtex(doi)
            bib_entries.append(bib)
            
            if args.rename:
                bib_data = parse_bibtex(bib)
                old_file = args.dir / paper["file"]
                if old_file.exists():
                    new_path = rename_paper(old_file, bib_data)
                    print(f"  [RENAME] -> {new_path.name}")
                else:
                    print(f"  [WARNING] Original file not found at {old_file}")
                    
        except Exception as exc:
            print(f"[ERROR] Failed for {paper.get('file')}: {exc}")
        time.sleep(args.delay)

    if not bib_entries:
        print("[INFO] No BibTeX entries were fetched.")
        return

    try:
        write_bibtex(bib_entries, args.output)
        print(f"[DONE] Saved {len(bib_entries)} entries to {args.output}")
    except Exception as exc:
        print(f"[ERROR] Could not write output file: {exc}")

if __name__ == "__main__":
    main()
