import argparse
import json
import time
import urllib.request
from pathlib import Path
from typing import List, Dict, Any

def load_papers(json_path: Path) -> List[Dict[str, Any]]:
    """Load the JSON file produced by ``extract_bib_info.py``.

    Parameters
    ----------
    json_path: Path
        Path to the JSON file.

    Returns
    -------
    List[Dict[str, Any]]
        List of paper dictionaries.
    """
    if not json_path.is_file():
        raise FileNotFoundError(f"Input file not found: {json_path}")
    with json_path.open(encoding="utf-8") as f:
        return json.load(f)

def fetch_bibtex(doi: str, timeout: int = 10) -> str:
    """Retrieve a BibTeX entry for a DOI.

    Parameters
    ----------
    doi: str
        DOI string (e.g. ``10.1109/XYZ.2023.123456``).
    timeout: int, optional
        Seconds to wait for the HTTP request.

    Returns
    -------
    str
        Raw BibTeX text.
    """
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8")

def write_bibtex(entries: List[str], output_path: Path) -> None:
    """Write a list of BibTeX entries to ``output_path``.

    The function creates the parent directory if necessary.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for entry in entries:
            f.write(entry.rstrip() + "\n\n")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch BibTeX entries for papers that have a DOI."
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
        "--delay",
        type=float,
        default=1.0,
        help="Seconds to wait between requests to be kind to the DOI service (default: 1.0).",
    )
    args = parser.parse_args()

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
        except Exception as exc:
            print(f"[ERROR] Failed to fetch DOI {doi}: {exc}")
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
