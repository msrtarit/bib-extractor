import argparse
import json
import time
import urllib.request
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

def load_papers(json_path: Path) -> List[Dict[str, Any]]:
    """Load the JSON file produced by ``extract_bib_info.py``."""
    if not json_path.is_file():
        raise FileNotFoundError(f"Input file not found: {json_path}")
    with json_path.open(encoding="utf-8") as f:
        return json.load(f)

def fetch_bibtex(doi: str, timeout: int = 10) -> str:
    """Retrieve a BibTeX entry for a DOI, trying multiple APIs."""
    apis = [
        {"name": "doi.org", "url": f"https://doi.org/{doi}", "headers": {"Accept": "application/x-bibtex"}},
        {"name": "Crossref", "url": f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex", "headers": {}}
    ]
    
    for api in apis:
        try:
            req = urllib.request.Request(api["url"], headers=api["headers"])
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    return response.read().decode("utf-8")
        except Exception:
            continue
    raise Exception(f"Failed to fetch BibTeX for {doi} from all available APIs.")

def parse_bibtex(bib: str) -> Dict[str, str]:
    """Simple regex‑based parser to extract key fields from a BibTeX entry."""
    data = {}
    # Fields to extract
    fields = ["title", "year", "author", "journal", "volume", "number", "pages", "publisher"]
    for field in fields:
        match = re.search(f"{field}\\s*=\\s*[\\{{\"](.*?)[\\}}\"]", bib, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            content = re.sub(r"[\{\}]", "", content)
            data[field] = content
    return data

def generate_citation(bib_data: Dict[str, str], style: str = "apa") -> str:
    """Generate a simple citation string from BibTeX data."""
    author = bib_data.get("author", "Unknown Author")
    year = bib_data.get("year", "n.d.")
    title = bib_data.get("title", "Unknown Title")
    journal = bib_data.get("journal", bib_data.get("publisher", ""))
    volume = bib_data.get("volume", "")
    number = bib_data.get("number", "")
    pages = bib_data.get("pages", "")
    
    # Handle multiple authors
    authors_list = author.split(" and ")
    
    if style.lower() == "apa":
        # APA: "Smith, J., & Jones, M. (Year). Title. Journal."
        if len(authors_list) > 1:
            author_str = ", ".join(authors_list[:-1]) + " & " + authors_list[-1]
        else:
            author_str = authors_list[0]
        citation = f"{author_str} ({year}). {title}."
        if journal:
            citation += f" {journal}."

    elif style.lower() == "mla":
        # MLA: "Author. \"Title.\" Journal, Year."
        if len(authors_list) > 1:
            author_str = ", ".join(authors_list[:-1]) + ", and " + authors_list[-1]
        else:
            author_str = authors_list[0]
        citation = f"{author_str}. \"{title}.\" {journal}, {year}."

    elif style.lower() == "ieee":
        # IEEE: "Author(s), \"Title,\" Journal, vol. x, no. x, pp. x, Year."
        formatted_authors = []
        for a in authors_list:
            if "," in a: # Last, First
                parts = a.split(",")
                last = parts[0].strip()
                first = parts[1].strip()
                formatted_authors.append(f"{first[0]}. {last}")
            else: # First Last
                parts = a.split()
                if len(parts) > 1:
                    formatted_authors.append(f"{parts[0][0]}. {parts[-1]}")
                else:
                    formatted_authors.append(a)
        
        if len(formatted_authors) > 1:
            author_str = ", ".join(formatted_authors[:-1]) + " and " + formatted_authors[-1]
        else:
            author_str = formatted_authors[0]
            
        citation = f"{author_str}, \"{title},\" {journal}"
        if volume: citation += f", vol. {volume}"
        if number: citation += f", no. {number}"
        if pages: citation += f", pp. {pages}"
        citation += f", {year}."

    else:
        author_str = " and ".join(authors_list)
        citation = f"{author_str}, {title} ({year})."
    
    return citation

def sanitize_filename(filename: str) -> str:
    """Remove characters that are invalid in filenames."""
    return re.sub(r'[/\\:*?"<>|]', "", filename)

def rename_paper(old_path: Path, bib_data: Dict[str, str]) -> Path:
    """Rename a PDF file based on BibTeX data."""
    if not old_path.exists():
        return old_path

    year = bib_data.get("year", "UnknownYear")
    author = bib_data.get("author", "UnknownAuthor").split(" and ")[0].split(",")[0]
    title = bib_data.get("title", "UnknownTitle")
    
    new_name = f"{year} - {author} - {title[:60]}"
    new_name = sanitize_filename(new_name) + ".pdf"
    new_path = old_path.parent / new_name
    
    if old_path != new_path:
        counter = 1
        final_path = new_path
        while final_path.exists():
            final_path = new_path.with_name(f"{new_path.stem}_{counter}.pdf")
            counter += 1
        old_path.rename(final_path)
        return final_path
    return old_path

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=40, fill='█'):
    """Call in a loop to create terminal progress bar."""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch BibTeX and citations for papers, with optional auto-renaming."
    )
    parser.add_argument("--input", type=Path, default=Path("paper_info.json"), help="Input JSON file.")
    parser.add_argument("--output", type=Path, default=Path("papers.bib"), help="Output BibTeX file.")
    parser.add_argument("--citations", type=Path, help="Output file for formatted citations.")
    parser.add_argument("--style", type=str, default="apa", choices=["apa", "mla", "ieee"], help="Citation style.")
    parser.add_argument("--rename", action="store_true", help="Rename original PDFs.")
    parser.add_argument("--dir", type=Path, help="Directory of original PDFs.")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests.")
    args = parser.parse_args()

    if args.rename and not args.dir:
        print("[ERROR] You must provide --dir when using --rename.")
        return

    try:
        papers = load_papers(args.input)
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return

    bib_entries: List[str] = []
    citations: List[str] = []
    total = len(papers)
    
    print(f"Processing {total} papers...")
    for i, paper in enumerate(papers):
        doi = paper.get("doi")
        print_progress_bar(i + 1, total, prefix='Progress:', suffix=f'Complete ({paper.get("file", "...")})', length=30)
        
        if not doi:
            continue
            
        try:
            bib = fetch_bibtex(doi)
            bib_entries.append(bib)
            bib_data = parse_bibtex(bib)
            
            if args.citations:
                citations.append(generate_citation(bib_data, args.style))
            
            if args.rename:
                old_file = args.dir / paper["file"]
                if old_file.exists():
                    rename_paper(old_file, bib_data)
                    
        except Exception:
            pass # Silently skip errors during progress bar view
        time.sleep(args.delay)

    # Save BibTeX
    if bib_entries:
        output_path = args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            for entry in bib_entries:
                f.write(entry.rstrip() + "\n\n")
        print(f"[DONE] Saved {len(bib_entries)} BibTeX entries to {args.output}")

    # Save Citations
    if citations:
        with args.citations.open("w", encoding="utf-8") as f:
            for citation in citations:
                f.write(citation + "\n\n")
        print(f"[DONE] Saved {len(citations)} citations ({args.style.upper()}) to {args.citations}")

if __name__ == "__main__":
    main()
