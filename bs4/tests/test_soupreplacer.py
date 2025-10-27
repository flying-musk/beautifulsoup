# bs4/tests/test_soupreplacer.py
from bs4 import BeautifulSoup

try:
    from bs4 import SoupReplacer
except Exception:
    from bs4.filter import SoupReplacer


def _soup(html, **kwargs):
    try:
        return BeautifulSoup(html, "lxml", **kwargs)
    except Exception:
        return BeautifulSoup(html, "html.parser", **kwargs)


def test_replace_b_to_blockquote():
    html = "<p>Hi <b>Mars</b>!</p>"
    soup = _soup(html, replacer=SoupReplacer("b", "blockquote"))
    assert soup.find("b") is None
    node = soup.find("blockquote")
    assert node is not None
    assert node.get_text() == "Mars"


def test_replace_p_to_div_keep_attrs_and_text():
    html = "<div><p class='x'>A</p><p>B</p></div>"
    soup = _soup(html, replacer=SoupReplacer("p", "div"))
    assert soup.find("p") is None
    inner_divs = soup.select("div > div")
    assert len(inner_divs) == 2
    assert inner_divs[0].get("class") == ["x"]
    assert inner_divs[0].get_text() == "A"
    assert inner_divs[1].get_text() == "B"
