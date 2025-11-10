# bs4/tests/test_soupreplacer_m3.py
from bs4 import BeautifulSoup

try:
    from bs4 import SoupReplacer
except Exception:
    from bs4.filter import SoupReplacer


def _soup(markup: str, **kwargs):
    try:
        return BeautifulSoup(markup, "lxml", **kwargs)
    except Exception:
        return BeautifulSoup(markup, "html.parser", **kwargs)


def test_pair_mode_rename_removes_original_tags():
    soup = _soup("<div><b>Hello</b></div>", replacer=SoupReplacer("b", "blockquote"))
    assert soup.find("b") is None
    assert soup.find("blockquote").get_text() == "Hello"


def test_name_xformer_preserves_sibling_structure():
    replacer = SoupReplacer(
        name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name
    )
    soup = _soup("<div><b>one</b><span>two</span></div>", replacer=replacer)
    outer_div = soup.find("div")
    children = [child for child in outer_div.children if getattr(child, "name", None)]
    assert [child.name for child in children] == ["blockquote", "span"]
    assert children[0].get_text() == "one"
    assert children[1].get_text() == "two"


def test_name_xformer_handles_nested_tags():
    replacer = SoupReplacer(
        name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name
    )
    soup = _soup("<div><b>Outer <b>Inner</b></b></div>", replacer=replacer)
    blocks = soup.find_all("blockquote")
    assert len(blocks) == 2
    assert blocks[0].find("blockquote") == blocks[1]


def test_attrs_xformer_adds_class():
    def add_test_class(tag):
        if tag.name == "p":
            attrs = dict(tag.attrs)
            classes = attrs.get("class", [])
            if isinstance(classes, str):
                classes = [classes]
            attrs["class"] = list(classes) + ["test"]
            return attrs
        return tag.attrs

    soup = _soup("<p>hello</p>", replacer=SoupReplacer(attrs_xformer=add_test_class))
    assert soup.find("p").get("class") == ["test"]


def test_attrs_xformer_remove_attr():
    def remove_class(tag):
        if "class" in tag.attrs:
            attrs = dict(tag.attrs)
            attrs.pop("class", None)
            return attrs
        return tag.attrs

    soup = _soup("<b class='x'>bold</b>", replacer=SoupReplacer(attrs_xformer=remove_class))
    tag = soup.find("b") or soup.find("blockquote")
    assert tag.get("class") is None


def test_xformer_side_effect_mutates_in_place():
    def add_marker(tag):
        if tag.name == "div":
            tag["data-test"] = "1"

    soup = _soup("<div><p>text</p></div>", replacer=SoupReplacer(xformer=add_marker))
    assert soup.find("div")["data-test"] == "1"


def test_xformer_can_remove_attr_in_place():
    def remove_class_attr(tag):
        if tag.name == "p" and "class" in tag.attrs:
            del tag.attrs["class"]

    soup = _soup("<p class='x y'>t</p>", replacer=SoupReplacer(xformer=remove_class_attr))
    p = soup.find("p")
    assert p.get("class") is None
    assert p.get_text() == "t"


def test_xformer_remove_attr_is_noop_when_absent():
    def remove_class_attr(tag):
        if "class" in tag.attrs:
            del tag.attrs["class"]

    soup = _soup("<p id='k'>t</p>", replacer=SoupReplacer(xformer=remove_class_attr))
    p = soup.find("p")
    assert p.get("class") is None
    assert p.get("id") == "k"


def test_replacer_resets_between_parses():
    replacer = SoupReplacer("b", "blockquote")
    soup_one = _soup("<b>first</b>", replacer=replacer)
    assert soup_one.find("blockquote").get_text() == "first"

    soup_two = _soup("<b>second</b>", replacer=replacer)
    assert soup_two.find("blockquote").get_text() == "second"
