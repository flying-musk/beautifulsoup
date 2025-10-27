# apps/m2/task3.py
import sys
from bs4 import BeautifulSoup, SoupStrainer, element


def pick_parser():
    try:
        import lxml  # noqa: F401

        return "lxml"
    except Exception:
        return "html.parser"


def main():
    if len(sys.argv) < 2:
        print("Usage: python task3.py <input.html>")
        return

    path = sys.argv[1]
    with open(path, "rb") as f:
        data = f.read()

    strainer = SoupStrainer(True)
    soup = BeautifulSoup(data, pick_parser(), parse_only=strainer)

    for node in soup.descendants:
        if isinstance(node, element.Tag):
            print(node.name)


if __name__ == "__main__":
    main()
