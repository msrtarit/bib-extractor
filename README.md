# Bib Extractor

[![PyPI version](https://img.shields.io/pypi/v/bib-extractor.svg?color=blue)](https://pypi.org/project/bib-extractor/)
[![License: MIT](https://img.shields.io/pypi/l/bib-extractor.svg?color=green)](https://pypi.org/project/bib-extractor/)

A tiny, **pip‑installable** Python utility that scans a folder of PDF papers, extracts their DOI (or a title fallback), and produces a JSON file that can be turned into a BibTeX bibliography.

---

## ✨ Features
- Works on any folder of PDFs.
- **Pure Python**: No external tools like Poppler or `pdftotext` required.
- Detects DOI strings with a robust regular expression.
- **Multiple API Support**: Queries `doi.org` and falls back to **Crossref** for metadata.
- **Auto-Rename**: Automatically renames PDFs to `Year - Author - Title.pdf`.
- **Formatted Citations**: Generates **APA/MLA** style reference lists in a separate text file.
- **Visual Progress**: Includes a terminal progress bar for high‑volume processing.

---

## 📦 Installation
### From PyPI (recommended)
```bash
pip install bib-extractor
```

### From source
1. **Clone the repository**
```bash
git clone https://github.com/msrtarit/bib_extractor.git
cd bib_extractor
```
2. (Optional) Create a virtual environment and install the package in editable mode:
```bash
python -m venv .venv
.venv\\Scripts\\activate   # Windows
# or source .venv/bin/activate on Unix
pip install -e .
```

---

## 🚀 Usage
### Extract DOIs / titles
```bash
# Using the installed command (if installed via pip)
bib-extractor --dir path/to/papers --output paper_info.json

# Or run the script directly from the source checkout
python -m bib_extractor.extract_bib_info --dir path/to/papers --output paper_info.json
```
- `--dir` defaults to the current working directory.
- `--output` defaults to `paper_info.json`.

### Fetch BibTeX entries & Auto-Rename
```bash
# Fetch entries and automatically rename your PDFs
bib-fetch --input paper_info.json --output papers.bib --rename --dir path/to/papers
```
- `--input`: The JSON file from the extractor.
- `--output`: The destination `.bib` file.
- `--citations`: (Optional) Output file for a formatted reference list (e.g., `refs.txt`).
- `--style`: (Optional) Citation style for the list (`apa` or `mla`, default is `apa`).
- `--rename`: (Optional) Automatically renames the files in `--dir` to a standard format: `Year - Author - Title.pdf`.
- `--dir`: (Required if renaming) The folder where your original PDFs are located.

---

## 🤝 Contributing
Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to fork the repo, set up a development environment, and submit pull requests.

---

## 📜 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
