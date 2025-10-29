# apps/m2/task6.py
import sys
from bs4 import BeautifulSoup

try:
    from bs4 import SoupReplacer
except Exception:
    from bs4.filter import SoupReplacer


def pick_parser(input_path: str) -> str:
    is_xml = input_path.lower().endswith(".xml")
    try:
        import lxml  # noqa: F401

        return "lxml-xml" if is_xml else "lxml"
    except Exception:
        return "xml" if is_xml else "html.parser"


def main():
    if len(sys.argv) != 3:
        print(
            'Usage: PYTHONPATH="$PWD" python3 apps/m2/task6.py <input.(xml|html)> <output.(xml|html)>'
        )
        sys.exit(1)

    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, "rb") as f:
        markup = f.read()

    replacer = SoupReplacer("b", "blockquote")
    soup = BeautifulSoup(markup, features=pick_parser(inp), replacer=replacer)

    with open(outp, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print(f"✅ Done. Wrote: {outp}")


if __name__ == "__main__":
    main()
