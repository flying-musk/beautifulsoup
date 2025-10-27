# apps/m2/task4.py
import sys
from bs4 import BeautifulSoup, SoupStrainer


def pick_parser():
    try:
        import lxml  # noqa: F401

        return "lxml"
    except Exception:
        return "html.parser"


def main():
    if len(sys.argv) < 2:
        print("Usage: python task4.py <input.html>")
        return

    path = sys.argv[1]
    with open(path, "rb") as f:
        data = f.read()

    strainer = SoupStrainer(id=True)
    soup = BeautifulSoup(data, pick_parser(), parse_only=strainer)

    for tag in soup.find_all(True, id=True):
        print(f"{tag.name} {tag.get('id')}")


if __name__ == "__main__":
    main()
