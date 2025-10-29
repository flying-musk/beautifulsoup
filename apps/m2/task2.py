# apps/m2/task2.py
import sys
import os
from bs4 import BeautifulSoup, SoupStrainer


def detect_file_type(file_path):
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
        print("Usage: python3 task2.py <input.html|input.xml>")
        return

    path = sys.argv[1]

    file_type = detect_file_type(path)
    parser = pick_parser(file_type)

    print(f"Processing {file_type.upper()} file: {path}")
    print(f"Using parser: {parser}")

    with open(path, "rb") as f:
        data = f.read()

    if file_type == "xml":
        # In XML, links might be in <link> tags or <a> tags
        strainer = SoupStrainer(["a", "link"])
        soup = BeautifulSoup(data, parser, parse_only=strainer)

        # Find both <a> and <link> tags
        for tag in soup.find_all(["a", "link"]):
            href = tag.get("href", "")
            text = tag.get_text(strip=True) or ""
            tag_name = tag.name
            print(f"[{tag_name}] {href} | {text}")
    else:
        only_a = SoupStrainer("a")
        soup = BeautifulSoup(data, parser, parse_only=only_a)

        for a in soup.find_all("a"):
            href = a.get("href", "")
            text = a.get_text(strip=True) or ""
            print(f"{href} | {text}")


if __name__ == "__main__":
    main()
