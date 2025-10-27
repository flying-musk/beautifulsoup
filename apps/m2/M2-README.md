# Milestone 2 – Part 2

## API Definitions (Milestone 1 & 2 Part 1)

| Function | File | Line | Description |
|-----------|------|------|-------------|
| BeautifulSoup.__init__ | bs4/__init__.py | L133 | Initializes parser, handles `parse_only` (SoupStrainer). |
| Tag.find_all | bs4/element.py | L2715 | Finds all tags matching name/attributes. |
| Tag.find_parent | bs4/element.py | L992 | Finds the nearest parent tag matching criteria. |
| Tag.prettify | bs4/element.py | L2601 | Converts parse tree to formatted HTML. |
| Tag.select | bs4/element.py | L2799 | CSS selector support. |
| Tag.get_text | bs4/element.py | L524 | Extracts inner text content. |
| Tag.decompose | bs4/element.py | L635 | Removes the tag and its contents from tree. |
| PageElement.descendants | bs4/element.py | L2764 | Generator over all descendant nodes (used in M2 task3). |
| SoupStrainer.__init__ | bs4/filter.py | L313 | Filters nodes during parsing to improve performance. |

---

**Notes**

- Line numbers are based on the original `beautifulsoup.zip` source code provided in Canvas.  
- These APIs were used across Milestone 1 and Milestone 2 (Part 1) to perform:  
  - HTML/XML parsing  
  - Tag searching (`find_all`, `find_parent`, `select`)  
  - Tree manipulation (`decompose`, `prettify`)  
  - Text extraction (`get_text`)  
  - Traversal using iterators (`descendants`)
  - Performance optimization (`SoupStrainer`)
