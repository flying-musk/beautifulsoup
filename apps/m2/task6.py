# apps/m2/task6_replacer.py
import sys
from bs4 import BeautifulSoup

try:
    from bs4 import SoupReplacer
except Exception:
    from bs4.filter import SoupReplacer


def pick_parser():
    try:
        import lxml  # noqa: F401

        return "lxml"
    except Exception:
        return "html.parser"


def main():
    if len(sys.argv) < 3:
        print("Usage: python task6_replacer.py <input.html> <output.html>")
        return

    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, "rb") as f:
        html = f.read()

    replacer = SoupReplacer("b", "blockquote")
    soup = BeautifulSoup(html, pick_parser(), replacer=replacer)

    with open(outp, "w", encoding="utf-8") as f:
        f.write(soup.prettify())


if __name__ == "__main__":
    main()
