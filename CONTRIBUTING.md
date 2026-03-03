# Contributing to Bib Extractor

Thank you for considering contributing to **Bib Extractor**! 🎉

## How to Get Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/msrtarit/bib_extractor.git
   cd bib_extractor
   ```
3. **Create a new branch** for your change:
   ```bash
   git checkout -b my-feature-or-fix
   ```

## Development Setup

- The project uses only the Python standard library, so no extra packages are required.
- You do need **Poppler** (`pdftotext`) installed on your system to run the extractor. See the README for installation instructions.

## Code Style & Linting

- Follow the existing code style (PEP 8). The CI workflow runs `flake8` with the following settings:
  - Max line length: **127** characters
  - Max complexity: **10**
- Run lint locally before committing:
  ```bash
  flake8 .
  ```

## Testing

There are currently no automated tests, but you can manually verify the workflow:
1. Run the extractor on a sample folder of PDFs.
2. Run `fetch_bibtex.py` to generate a `.bib` file.
3. Ensure the output JSON and BibTeX files look correct.

If you add tests in the future, place them in a `tests/` directory and configure a test runner (e.g., `pytest`).

## Submitting a Pull Request

1. **Commit your changes** with clear, concise messages.
2. **Push** the branch to your fork:
   ```bash
   git push origin my-feature-or-fix
   ```
3. Open a **Pull Request** against the `main` branch of the original repository.
4. Fill out the PR template (if present) and describe the changes.
5. The CI workflow will automatically run linting. Make sure it passes before merging.

## Reporting Issues

If you encounter a bug or have a feature request, please open an issue on GitHub with:
- A clear title.
- Steps to reproduce (for bugs).
- Expected vs. actual behavior.
- Any relevant logs or screenshots.

## License

By contributing, you agree that your contributions will be licensed under the same **MIT License** as the project.

---

Happy coding! 🚀
