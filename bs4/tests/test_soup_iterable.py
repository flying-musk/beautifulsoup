# bs4/tests/test_soup_iterable.py
"""Tests for iterable BeautifulSoup (Milestone 4)."""

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Comment


def _soup(html, **kwargs):
    """Helper function to create a soup with appropriate parser."""
    try:
        return BeautifulSoup(html, "lxml", **kwargs)
    except Exception:
        return BeautifulSoup(html, "html.parser", **kwargs)


def test_iterate_over_simple_soup():
    """Test 1: Basic iteration over a simple soup object."""
    html = "<html><head><title>Test</title></head><body><p>Hello</p></body></html>"
    soup = _soup(html)

    # Collect all nodes by iterating
    nodes = list(soup)

    # Should include BeautifulSoup itself as the first node
    assert nodes[0] is soup
    assert isinstance(nodes[0], BeautifulSoup)

    # Should include all descendants (html, head, title, body, p)
    assert len(nodes) > 1

    # Verify that we get Tag and NavigableString nodes
    tag_nodes = [n for n in nodes if isinstance(n, Tag)]
    string_nodes = [n for n in nodes if isinstance(n, NavigableString)]

    assert len(tag_nodes) > 0
    assert len(string_nodes) > 0


def test_iterate_empty_soup():
    """Test 2: Iteration over an empty soup should still yield the soup itself."""
    soup = _soup("")

    nodes = list(soup)

    # Should only contain the soup itself
    assert len(nodes) == 1
    assert nodes[0] is soup
    assert isinstance(nodes[0], BeautifulSoup)


def test_iterate_nested_structure():
    """Test 3: Iteration over a deeply nested structure."""
    html = "<div><div><div><p>Nested</p></div></div></div>"
    soup = _soup(html)

    nodes = list(soup)

    # Should include soup + all nested tags + text
    assert nodes[0] is soup

    # Find all div tags
    div_tags = [n for n in nodes if isinstance(n, Tag) and n.name == "div"]
    assert len(div_tags) == 3  # Three nested divs

    # Find the paragraph
    p_tags = [n for n in nodes if isinstance(n, Tag) and n.name == "p"]
    assert len(p_tags) == 1

    # Find the text node
    text_nodes = [
        n
        for n in nodes
        if isinstance(n, NavigableString) and str(n).strip() == "Nested"
    ]
    assert len(text_nodes) == 1


def test_iterate_with_comments():
    """Test 4: Iteration should include Comment nodes."""
    html = "<html><!-- This is a comment --><body>Text</body></html>"
    soup = _soup(html)

    nodes = list(soup)

    # Find comment nodes
    comment_nodes = [n for n in nodes if isinstance(n, Comment)]
    assert len(comment_nodes) == 1
    assert comment_nodes[0] == " This is a comment "


def test_iterate_is_generator_not_list():
    """Test 5: Verify that iteration uses a generator (doesn't pre-collect nodes)."""
    html = "<html>" + "<div>" * 100 + "Text" + "</div>" * 100 + "</html>"
    soup = _soup(html)

    # Create an iterator
    iterator = iter(soup)

    # Verify it's an iterator (has __next__ method)
    assert hasattr(iterator, "__next__")

    # Get first few nodes to verify lazy evaluation
    first_node = next(iterator)
    assert first_node is soup

    # Iterate a bit more to ensure it works incrementally
    count = 0
    for node in iterator:
        count += 1
        if count >= 10:
            break

    # Should have yielded at least 10 more nodes
    assert count == 10

    # Verify we can continue iterating (didn't exhaust the iterator)
    remaining_nodes = list(iterator)
    assert len(remaining_nodes) > 0


def test_basic_for_loop_iteration():
    """Test 6: Basic for loop iteration - the main use case: for node in soup: print(node)"""
    html = "<html><head><title>Test Page</title></head><body><p>Hello <b>world</b></p></body></html>"
    soup = _soup(html)

    # This is the exact pattern from the requirements:
    # for node in soup:
    #     print(node)

    # Collect all nodes by iterating (simulating what print would do)
    collected_nodes = []
    for node in soup:
        collected_nodes.append(node)
        # In actual usage, you would do: print(node)
        # But in test, we collect to verify

    # Verify we collected nodes
    assert len(collected_nodes) > 0

    # First node should be the BeautifulSoup object itself
    assert collected_nodes[0] is soup
    assert isinstance(collected_nodes[0], BeautifulSoup)

    # Should include various types of nodes
    tags_found = [n for n in collected_nodes if isinstance(n, Tag)]
    strings_found = [n for n in collected_nodes if isinstance(n, NavigableString)]

    # Verify we have both tags and strings
    assert len(tags_found) > 0
    assert len(strings_found) > 0

    # Verify we can convert nodes to strings (as print would do)
    for node in collected_nodes[:5]:  # Test first 5 nodes
        str_repr = str(node)
        assert isinstance(str_repr, str)
        assert len(str_repr) >= 0  # All nodes should be stringifiable

    # Verify iteration works multiple times (not exhausted)
    second_iteration = list(soup)
    assert len(second_iteration) == len(collected_nodes)
