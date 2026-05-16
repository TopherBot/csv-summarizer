# csv‑summarizer

**Tiny utility** – parse a CSV file and output a quick summary.

## Features
- Validates input path before processing (idempotent checks).
- Graceful handling of missing files, empty files, and malformed CSV data.
- Optional numeric summary (mean, min, max) for selected columns.
- Clear, self‑documenting function names.

## Installation
```bash
# Requires Python 3.8+
git clone https://github.com/your‑org/csv‑summarizer.git
cd csv‑summarizer
pip install -r requirements.txt  # (none needed beyond the stdlib)
```

## Usage
```bash
python csv_summarizer.py path/to/file.csv        # basic summary
python csv_summarizer.py path/to/file.csv --numeric column1 column2  # numeric stats
```

## Design notes
- All I/O is wrapped in `try/except` blocks to avoid silent failures.
- The script performs a *pre‑flight* existence check before opening files, preventing name‑collision or silent‑creation errors.
- Functions follow a `verb_noun` naming scheme for readability.

---
*Happy coding!*