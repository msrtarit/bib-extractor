# Bib Extractor

[![PyPI version](https://badge.fury.io/py/bib-extractor.svg)](https://pypi.org/project/bib-extractor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tiny, **pip‑installable** Python utility that scans a folder of PDF papers, extracts their DOI (or a title fallback), and produces a JSON file that can be turned into a BibTeX bibliography.

---

## ✨ Features
- Works on any folder of PDFs.
- Uses `pdftotext` (Poppler) to read the first two pages of each PDF.
- Detects DOI strings with a robust regular expression.
- Falls back to the first few non‑empty lines as a title when no DOI is found.
- Command‑line interface with `--dir` and `--output` options.
- Zero external Python dependencies (standard library only).

---

## 📦 Installation
### From PyPI (recommended)
```bash
pip install bib-extractor
```
### From source
1. **Install Poppler** – `pdftotext` is required.
   - **Windows**: download from <https://github.com/oschwartz10612/poppler-windows/releases> and add the `bin` folder to your `PATH`.
   - **macOS**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils`
2. **Clone the repository**
```bash
git clone https://github.com/msrtarit/bib_extractor.git
cd bib_extractor
```
3. (Optional) Create a virtual environment and install the package in editable mode:
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
python extract_bib_info.py --dir path/to/papers --output paper_info.json
```
- `--dir` defaults to the current working directory.
- `--output` defaults to `paper_info.json`.

### Fetch BibTeX entries
```bash
# From the repository root (or after installing via pip)
python fetch_bibtex.py --input paper_info.json --output papers.bib
```
The script reads the JSON produced by the extractor, fetches BibTeX records for entries that have a DOI, and writes them to `papers.bib`.

The extractor prints progress and writes a JSON array like:
```json
[
  {"file": "1.pdf", "doi": "10.1109/XYZ.2023.123456"},
  {"file": "2.pdf", "title": "An Interesting Study on …"}
]
```

---

## Next steps
- Convert the generated `.bib` file to the citation style you need.
- Extend the workflow with additional scripts or integrate into your bibliography manager.

---

## 🤝 Contributing
Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to fork the repo, set up a development environment, and submit pull requests.

---

## 📜 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.


[![PyPI version](https://badge.fury.io/py/bib-extractor.svg)](https://pypi.org/project/bib-extractor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tiny, **pip‑installable** Python utility that scans a folder of PDF papers, extracts their DOI (or a title fallback), and produces a JSON file that can be turned into a BibTeX bibliography.

---

## ✨ Features
- Works on any folder of PDFs.
- Uses `pdftotext` (Poppler) to read the first two pages of each PDF.
- Detects DOI strings with a robust regular expression.
- Falls back to the first few non‑empty lines as a title when no DOI is found.
- Command‑line interface with `--dir` and `--output` options.
- Zero external Python dependencies (standard library only).

---

## 📦 Installation
### From PyPI (recommended)
```bash
pip install bib-extractor
```
### From source
1. **Install Poppler** – `pdftotext` is required.
   - **Windows**: download from <https://github.com/oschwartz10612/poppler-windows/releases> and add the `bin` folder to your `PATH`.
   - **macOS**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils`
2. **Clone the repository**
```bash
git clone https://github.com/msrtarit/bib_extractor.git
cd bib_extractor
```
3. (Optional) Create a virtual environment and install the package in editable mode:
```bash
python -m venv .venv
.venv\\Scripts\\activate   # Windows
# or source .venv/bin/activate on Unix
pip install -e .
```

---

## 🚀 Usage
```bash
# Using the installed command (if installed via pip)
bib-extractor --dir path/to/papers --output paper_info.json

# Or run the script directly from the source checkout
python extract_bib_info.py --dir path/to/papers --output paper_info.json
```
- `--dir` defaults to the current working directory.
- `--output` defaults to `paper_info.json`.

The script prints progress and writes a JSON array like:
```json
[
  {"file": "1.pdf", "doi": "10.1109/XYZ.2023.123456"},
  {"file": "2.pdf", "title": "An Interesting Study on …"}
]
```

---

## Next steps
- Feed the generated JSON into `fetch_bibtex.py` (included) to retrieve full BibTeX entries.
- Convert the resulting `.bib` file to the citation style you need.

---

## 🤝 Contributing
Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to fork the repo, set up a development environment, and submit pull requests.

---

## 📜 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
