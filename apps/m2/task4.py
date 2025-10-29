# apps/m2/task4.py
import sys
import os
from bs4 import BeautifulSoup, SoupStrainer


def detect_file_type(file_path):
    """Detect if file is HTML or XML based on extension and content."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".xml":
        return "xml"
    elif ext in [".html", ".htm"]:
        return "html"

    with open(file_path, "rb") as f:
        first_bytes = f.read(100)
        content = first_bytes.decode("utf-8", errors="ignore")

        if content.strip().startswith("<?xml"):
            return "xml"
        elif "<!DOCTYPE html" in content or "<html" in content:
            return "html"

    return "html"


def pick_parser(file_type):
    """Choose appropriate parser based on file type."""
    if file_type == "xml":
        try:
            import lxml  # noqa: F401

            return "xml"  # Use lxml XML parser
        except ImportError:
            return "xml"  # Use built-in XML parser
    else:  # HTML
        try:
            import lxml  # noqa: F401

            return "lxml"
        except ImportError:
            return "html.parser"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 task4.py <input.html|input.xml>")
        return

    path = sys.argv[1]

    file_type = detect_file_type(path)
    parser = pick_parser(file_type)

    print(f"Processing {file_type.upper()} file: {path}")
    print(f"Using parser: {parser}")

    with open(path, "rb") as f:
        data = f.read()

    strainer = SoupStrainer(id=True)
    soup = BeautifulSoup(data, parser, parse_only=strainer)

    print(f"\nAll tags with 'id' attribute in {file_type.upper()} file:")
    tags_with_id = soup.find_all(True, id=True)
    
    if tags_with_id:
        for tag in tags_with_id:
            print(f"{tag.name} id='{tag.get('id')}'")
    else:
        print("No tags with 'id' attribute found.")


if __name__ == "__main__":
    main()
