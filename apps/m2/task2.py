# apps/m2/task2.py
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
        print("Usage: python task2.py <input.html>")
        return
    path = sys.argv[1]
    with open(path, "rb") as f:
        data = f.read()

    only_a = SoupStrainer("a")
    soup = BeautifulSoup(data, pick_parser(), parse_only=only_a)

    for a in soup.find_all("a"):
        href = a.get("href", "")
        text = a.get_text(strip=True) or ""
        print(f"{href} | {text}")


if __name__ == "__main__":
    main()
