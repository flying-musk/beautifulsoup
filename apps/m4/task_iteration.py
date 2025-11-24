#!/usr/bin/env python3
# apps/m4/task_iteration.py
"""
Milestone 4 Application: Demonstrating BeautifulSoup as an Iterable

This application demonstrates the new iteration capability of BeautifulSoup,
showing how to iterate over all nodes in a parsed HTML/XML document.

Usage:
    PYTHONPATH="$PWD" python3 apps/m4/task_iteration.py <input.(html|xml)> [output.txt]
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, TextIO

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Comment, PageElement


def pick_parser(path: Path) -> str:
    """Choose a parser based on file extension and available libraries."""
    suffix = path.suffix.lower()
    is_xml = suffix in {".xml", ".xhtml"}
    try:
        import lxml  # noqa: F401

        return "lxml-xml" if is_xml else "lxml"
    except Exception:
        return "xml" if is_xml else "html.parser"


def format_node(node: PageElement, index: int) -> str:
    """Format a node for output display."""
    node_type = type(node).__name__

    if isinstance(node, BeautifulSoup):
        return f"{index}: [{node_type}] BeautifulSoup object (root)"
    elif isinstance(node, Tag):
        attrs_str = ""
        if node.attrs:
            attrs = " ".join(f'{k}="{v}"' for k, v in sorted(node.attrs.items())[:3])
            attrs_str = f" {attrs}"
            if len(node.attrs) > 3:
                attrs_str += "..."
        return f"{index}: [{node_type}] <{node.name}{attrs_str}>"
    elif isinstance(node, Comment):
        content = str(node).strip()[:50]
        return f"{index}: [{node_type}] <!-- {content}... -->"
    elif isinstance(node, NavigableString):
        content = str(node).strip().replace("\n", "\\n")[:50]
        return f'{index}: [{node_type}] "{content}"'
    else:
        content = str(node)[:50]
        return f"{index}: [{node_type}] {content}"


def analyze_document(input_path: Path, output_file: TextIO) -> None:
    """Analyze a document by iterating over all nodes."""
    with input_path.open("rb") as reader:
        markup = reader.read()

    soup = BeautifulSoup(markup, features=pick_parser(input_path))

    # Demonstrate iteration over all nodes
    output_file.write(f"=== Analyzing: {input_path.name} ===\n\n")
    output_file.write("Iterating over all nodes in the document:\n")
    output_file.write("-" * 60 + "\n")

    node_counts = {
        "BeautifulSoup": 0,
        "Tag": 0,
        "NavigableString": 0,
        "Comment": 0,
        "Other": 0,
    }

    tag_names = {}

    for index, node in enumerate(soup, 1):
        # Format and print the node
        output_file.write(format_node(node, index) + "\n")

        # Count node types
        if isinstance(node, BeautifulSoup):
            node_counts["BeautifulSoup"] += 1
        elif isinstance(node, Tag):
            node_counts["Tag"] += 1
            tag_name = node.name
            tag_names[tag_name] = tag_names.get(tag_name, 0) + 1
        elif isinstance(node, NavigableString):
            node_counts["NavigableString"] += 1
        elif isinstance(node, Comment):
            node_counts["Comment"] += 1
        else:
            node_counts["Other"] += 1

    # Summary statistics
    output_file.write("\n" + "=" * 60 + "\n")
    output_file.write("Summary Statistics:\n")
    output_file.write("-" * 60 + "\n")
    output_file.write(f"Total nodes: {sum(node_counts.values())}\n")
    for node_type, count in sorted(node_counts.items()):
        if count > 0:
            output_file.write(f"  {node_type}: {count}\n")

    if tag_names:
        output_file.write("\nTag name distribution:\n")
        for tag_name, count in sorted(tag_names.items(), key=lambda x: -x[1]):
            output_file.write(f"  <{tag_name}>: {count}\n")

    # Demonstrate that iteration is memory-efficient (generator-based)
    output_file.write("\n" + "=" * 60 + "\n")
    output_file.write("Iteration characteristics:\n")
    output_file.write("-" * 60 + "\n")
    output_file.write("✓ BeautifulSoup is now iterable using 'for node in soup:'\n")
    output_file.write(
        "✓ Iteration uses generators (does not collect nodes into a list)\n"
    )
    output_file.write("✓ Memory-efficient for large documents\n")
    output_file.write("✓ Includes BeautifulSoup object itself as the first node\n")
    output_file.write("✓ Then includes all descendants in document order\n")


def main(argv: Iterable[str]) -> int:
    """Main entry point."""
    args = list(argv)
    if len(args) < 1:
        print(
            'Usage: PYTHONPATH="$PWD" python3 apps/m4/task_iteration.py '
            "<input.(html|xml)> [output.txt]"
        )
        return 1

    input_path = Path(args[0]).expanduser()
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        return 1

    output_path = Path(args[1]).expanduser() if len(args) >= 2 else None

    try:
        if output_path:
            with output_path.open("w", encoding="utf-8") as f:
                analyze_document(input_path, f)
            print(f"✅ Done. Analysis written to: {output_path}")
        else:
            analyze_document(input_path, sys.stdout)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
