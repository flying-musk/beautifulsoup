# Milestone 2

This milestone continues from M1 and dives deeper into **BeautifulSoup's internals**, **SoupStrainer** performance filtering, and the creation of a new **SoupReplacer** feature for tag-level transformation during parsing.

## Overview

This milestone consists of three main parts:

1. **Part 1**: Implement SoupStrainer applications (Tasks 2, 3, 4) for performance optimization
2. **Part 2**: Document API definitions used in Milestone 1 and Part 1
3. **Part 3**: Create and implement SoupReplacer for parsing-time tag replacement (Task 6)

## Files Structure

```
apps/m2/
├── M2-README.md          # This documentation
├── task2.py             # Extract hyperlinks using SoupStrainer
├── task3.py             # List all tags using SoupStrainer  
├── task4.py             # Find tags with id attributes using SoupStrainer
└── task6.py             # Replace <b> with <blockquote> using SoupReplacer

bs4/
├── filter.py            # Contains SoupStrainer and SoupReplacer implementations
├── __init__.py          # Exports SoupReplacer
└── tests/
    └── test_soupreplacer.py  # Test cases for SoupReplacer
```

---

## Part 1 – SoupStrainer Applications

### Overview
Each app demonstrates how to use `SoupStrainer` to limit parsing scope and improve performance by parsing only the parts of the file that matter for the specific task.

### Tasks Implemented
- **Task 2**: Extract all hyperlinks (`<a>` tags) using `SoupStrainer("a")`
- **Task 3**: List all tag names in the document using `SoupStrainer(True)` 
- **Task 4**: Find all tags with `id` attributes using `SoupStrainer(id=True)`

### How to Run

```bash
# Task 2: Extract all hyperlinks (<a> tags)
python3 apps/m2/task2.py sample.html
python3 apps/m2/task2.py sample.xml

# Task 3: List all tag names in the document
python3 apps/m2/task3.py sample.html
python3 apps/m2/task3.py sample.xml

# Task 4: Find all tags with id attributes
python3 apps/m2/task4.py sample.html
python3 apps/m2/task4.py sample.xml
```

### Expected Output Examples

**Task 2** (Hyperlinks):
```
Processing HTML file: sample.html
Using parser: lxml
https://example.com | Example
/local/path | Local Link
https://openai.com | OpenAI
```

**Task 3** (All Tags):
```
Processing HTML file: sample.html
Using parser: lxml
All tags found in HTML file:
html
head
title
body
h1
a
br
p
b
script
```

**Task 4** (Tags with ID):
```
Processing HTML file: sample.html
Using parser: lxml
All tags with 'id' attribute in HTML file:
h1 id='mars'
div id='links-section'
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

**Important**: When developing inside the local BeautifulSoup repo, make sure Python loads your local bs4 module (instead of the system-installed one).

```bash
# Replace <b> tags with <blockquote> tags in HTML
PYTHONPATH="$PWD" python3 apps/m2/task6.py sample.html output.html

# Replace <b> tags with <blockquote> tags in XML  
PYTHONPATH="$PWD" python3 apps/m2/task6.py sample.xml output.xml
```

**Expected Behavior**: 
- Parses the input file and replaces every `<b>` tag with `<blockquote>` during parsing
- Outputs a prettified version of the modified markup
- Works with both HTML and XML files
- Shows success message: `✅ Done. Wrote: output.html`

**Example Input/Output**:
```html
<!-- Input -->
<p>Click <a href="https://openai.com"><b>OpenAI</b></a> for AI research.</p>

<!-- Output -->
<p>
 Click
 <a href="https://openai.com">
  <blockquote>
   OpenAI
  </blockquote>
 </a>
 for AI research.
</p>
```

### Testing SoupReplacer

Run the test suite to verify SoupReplacer functionality:

```bash
PYTHONPATH="$PWD" python3 -m pytest bs4/tests/test_soupreplacer.py -v
```

This will run tests for:
- Basic tag replacement (`<b>` → `<blockquote>`)
- Attribute preservation during replacement
- Multiple tag replacement scenarios

---

## Testing and Verification

### Quick Test Script

To verify all implementations work correctly, run this comprehensive test:

```bash
# Test SoupStrainer applications
echo "=== Testing Task 2 (Hyperlinks) ==="
python3 apps/m2/task2.py sample.html
python3 apps/m2/task2.py sample.xml

echo "=== Testing Task 3 (All Tags) ==="
python3 apps/m2/task3.py sample.html
python3 apps/m2/task3.py sample.xml

echo "=== Testing Task 4 (Tags with ID) ==="
python3 apps/m2/task4.py sample.html
python3 apps/m2/task4.py sample.xml

echo "=== Testing Task 6 (SoupReplacer) ==="
PYTHONPATH="$PWD" python3 apps/m2/task6.py sample.html test_output.html
PYTHONPATH="$PWD" python3 apps/m2/task6.py sample.xml test_output.xml

echo "=== Running SoupReplacer Tests ==="
PYTHONPATH="$PWD" python3 -m pytest bs4/tests/test_soupreplacer.py -v
```

### Expected Results

- **Task 2**: Should extract all `<a>` and `<link>` tags with their href attributes
- **Task 3**: Should list all tag names found in the document
- **Task 4**: Should find all tags that have an `id` attribute
- **Task 6**: Should replace `<b>` tags with `<blockquote>` tags and create output files
- **Tests**: Should pass all SoupReplacer test cases

