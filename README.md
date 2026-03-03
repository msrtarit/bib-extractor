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

### 1. Extract DOIs / Titles
This step scans your PDFs and creates a metadata JSON.

**Standard Command:**
```bash
bib-extractor --dir path/to/papers --output paper_info.json
```

**Windows / Path Fallback:**
If the command above says "not found", use the Python module directly:
```bash
python -m bib_extractor --dir path/to/papers --output paper_info.json
```

---

### 2. Fetch BibTeX & Auto-Rename
This step uses the JSON from step 1 to download metadata and (optionally) rename files.

**Standard Command:**
```bash
bib-fetch --input paper_info.json --output papers.bib --rename --dir path/to/papers
```

**Windows / Path Fallback:**
```bash
python -m bib_extractor.fetch_bibtex --input paper_info.json --output papers.bib --rename --dir path/to/papers
```

> [!TIP]
> **Windows Users**: If the short commands (`bib-extractor`) don't work, ensure your Python `Scripts` folder is added to your system environment variables. Alternatively, always use the `python -m` method shown above.
### 🛠️ Options & Arguments

| Flag | Description | Default |
| :--- | :--- | :--- |
| `--dir` | Directory containing PDF files (or where to rename) | Current Dir |
| `--output` | Path to save the BibTeX `.bib` file | `paper_info.json` |
| `--input` | The JSON metadata file from Step 1 | *Required for Step 2* |
| `--citations` | Output file for a formatted reference list (e.g. `refs.txt`) | Optional |
| `--style` | Citation style for the reference list (`apa` or `mla`) | `apa` |
| `--rename` | Automatically rename PDFs to `Year - Author - Title.pdf` | Optional |

---

## 🤝 Contributing
Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to fork the repo, set up a development environment, and submit pull requests.

---

## 📜 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
