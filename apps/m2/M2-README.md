# Milestone 2

This milestone continues from M1 and dives deeper into **BeautifulSoup’s internals**, **SoupStrainer** performance filtering, and the creation of a new **SoupReplacer** feature for tag-level transformation during parsing.

---

## Part 1 – SoupStrainer Applications

### How to Run

Each app demonstrates how to use `SoupStrainer` to limit parsing scope and improve performance.

```bash
# list all <a> tags
python3 apps/m2/task2.py sample.html

# list all tag names
python3 apps/m2/task3.py sample.html

# list all tags that have id attributes
python3 apps/m2/task4.py sample.html
```

## Milestone 2 – Part 2

### API Definitions (Milestone 1 & 2 Part 1)

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

**Notes**

- Line numbers are based on the original `beautifulsoup.zip` source code provided in Canvas.  
- These APIs were used across Milestone 1 and Milestone 2 (Part 1) to perform:  
  - HTML/XML parsing  
  - Tag searching (`find_all`, `find_parent`, `select`)  
  - Tree manipulation (`decompose`, `prettify`)  
  - Text extraction (`get_text`)  
  - Traversal using iterators (`descendants`)
  - Performance optimization (`SoupStrainer`)

## Part 3 – SoupReplacer (Parsing-Time Tag Replacement)

`SoupReplacer` is a new utility class, conceptually similar to `SoupStrainer`,
but instead of filtering tags, it **replaces tag names during parsing**.

### Implementation:

- Added `class SoupReplacer` in `bs4/filter.py`
- Updated `BeautifulSoup.__init__`, `handle_starttag`, and `handle_endtag` to support an optional `replacer` argument
- Exposed `SoupReplacer` in `bs4/__init__.py`
- Added dedicated test file `bs4/tests/test_soupreplacer.py`

#### Usage

```
from bs4 import BeautifulSoup, SoupReplacer

html = "<p>Hi <b>Mars</b>!</p>"
soup = BeautifulSoup(html, "lxml", replacer=SoupReplacer("b", "blockquote"))
print(soup.prettify())
```

Output (`b → blockquote`):

```
<p>
 Hi
 <blockquote>
  Mars
 </blockquote>
</p>
```

#### Running the App (Task 6)

If you are developing inside the local BeautifulSoup repo:

> Make sure Python loads your local bs4 module (instead of the system-installed one).

Run the app with:

```
PYTHONPATH="$PWD" python3 apps/m2/task6_replacer.py sample.html out.html
```

This will parse `sample.html` and output `out.html`,
where every `<b>` has been replaced with `<blockquote>` during parsing.
