#!/usr/bin/env python3
# apps/m3/task7.py
"""
Milestone 3 Task-7 application:
    - Reads an HTML/XML document
    - Uses SoupReplacer transformer API to ensure every <p> tag has class="test"
    - Writes the transformed markup to an output file

Usage:
    PYTHONPATH="$PWD" python3 apps/m3/task7.py <input.(html|xml)> <output.(html|xml)>
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from bs4 import BeautifulSoup

try:
    from bs4 import SoupReplacer
except Exception:  # pragma: no cover - fallback for unusual import paths
    from bs4.filter import SoupReplacer


def pick_parser(path: Path) -> str:
    """Choose a parser based on file extension and available libraries."""
    suffix = path.suffix.lower()
    is_xml = suffix in {".xml", ".xhtml"}
    try:
        import lxml  # noqa: F401

        return "lxml-xml" if is_xml else "lxml"
    except Exception:
        return "xml" if is_xml else "html.parser"


def _ensure_class_list(value: Any) -> List[str]:
    """Normalize a tag's class attribute to a mutable list."""
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple):
        return list(value)
    return [str(value)]


def soup_replacer_for_paragraphs() -> SoupReplacer:
    def add_test_class(tag) -> Optional[Dict[str, Any]]:
        if tag.name != "p":
            return None
        attrs: Dict[str, Any] = dict(tag.attrs)
        classes = _ensure_class_list(attrs.get("class"))
        if "test" not in classes:
            classes.append("test")
        attrs["class"] = classes
        return attrs

    return SoupReplacer(attrs_xformer=add_test_class)


def transform_file(input_path: Path, output_path: Path) -> None:
    with input_path.open("rb") as reader:
        markup = reader.read()

    replacer = soup_replacer_for_paragraphs()
    soup = BeautifulSoup(markup, features=pick_parser(input_path), replacer=replacer)

    with output_path.open("w", encoding="utf-8") as writer:
        writer.write(soup.prettify())


def main(argv: Iterable[str]) -> int:
    args = list(argv)
    if len(args) != 2:
        print(
            "Usage: PYTHONPATH=\"$PWD\" python3 apps/m3/task7.py <input.(html|xml)> <output.(html|xml)>"
        )
        return 1

    input_path = Path(args[0]).expanduser()
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        return 1

    output_path = Path(args[1]).expanduser()

    transform_file(input_path, output_path)
    print(f"✅ Done. Wrote: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

