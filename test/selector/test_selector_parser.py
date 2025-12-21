
import pytest
from cssselector import selector, ParseError, Selector_Element, Selector_Children, Selector_Son, Selector_MatchAnywhere, Selector_MatchLast, AttributeSelector_HasName, AttributeSelector_Equal, AttributeSelector_ContainsWithSeparator

def test_read_tag ():

  #...
  
  with pytest.raises(ParseError):
    selector._read_tag("", 0, 0)

  #...

  tag, index = selector._read_tag("*", 0, 1)
  assert tag == ""
  assert index == 1

  #...

  tag, index = selector._read_tag("abc def", 0, 7)
  assert tag == "abc"
  assert index == 3

  #...

  tag, index = selector._read_tag("[abc]", 0, 5)
  assert tag == ""
  assert index == 0

def test_read_class_and_id ():
  
  #...

  with pytest.raises(ParseError):
    selector._read_class_and_id("", 0, 0)
  
  #...

  with pytest.raises(ParseError):
    selector._read_class_and_id("-", 0, 1)

  #...

  identifier, index = selector._read_tag("abc def", 0, 7)
  assert identifier == "abc"
  assert index == 3

def test_read_separator ():
  
  #...

  separator, index = selector._read_separator(" > ", 0, 3)
  assert separator == " > "
  assert index == 3

def test_strip ():

  #...

  start, end = selector._strip("abc")
  assert start == 0
  assert end == 3

  #...

  start, end = selector._strip("  abc")
  assert start == 2
  assert end == 5

  #...

  start, end = selector._strip("abc  ")
  assert start == 0
  assert end == 3

  #...

  start, end = selector._strip("  abc  ")
  assert start == 2
  assert end == 5

def test_parse_selector ():

  #...

  with pytest.raises(ParseError):
    selector.parse_selector("")

  #...

  sel = selector.parse_selector("a", match_anywhere=True, match_children=True)
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Element)
  assert sel.selector.tag == "a"
  assert sel.selector.attribute_selectors == []

  #...

  sel = selector.parse_selector("a", match_anywhere=False, match_children=False)
  assert isinstance(sel, Selector_MatchLast)
  assert isinstance(sel.selector, Selector_Element)
  assert sel.selector.tag == "a"
  assert sel.selector.attribute_selectors == []

  #...

  sel = selector.parse_selector("a", match_anywhere=True, match_children=False)
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_MatchLast)
  assert isinstance(sel.selector.selector, Selector_Element)
  assert sel.selector.selector.tag == "a"
  assert sel.selector.selector.attribute_selectors == []

  #...

  sel = selector.parse_selector("a", match_anywhere=False, match_children=True)
  assert isinstance(sel, Selector_Element)
  assert sel.tag == "a"
  assert sel.attribute_selectors == []

  #...

  sel = selector.parse_selector("a.abc", match_anywhere=False, match_children=True)
  assert isinstance(sel, Selector_Element)
  assert sel.tag == "a"

  assert isinstance(sel.attribute_selectors, list)
  assert len(sel.attribute_selectors) == 1

  assert isinstance(sel.attribute_selectors[0], AttributeSelector_ContainsWithSeparator)
  assert sel.attribute_selectors[0].name == "class"
  assert sel.attribute_selectors[0].value == "abc"

  #...

  sel = selector.parse_selector("a#abc", match_anywhere=False, match_children=True)
  assert isinstance(sel, Selector_Element)
  assert sel.tag == "a"

  assert isinstance(sel.attribute_selectors, list)
  assert len(sel.attribute_selectors) == 1

  assert isinstance(sel.attribute_selectors[0], AttributeSelector_Equal)
  assert sel.attribute_selectors[0].name == "id"
  assert sel.attribute_selectors[0].value == "abc"

  #...

  sel = selector.parse_selector("a[a=\"1\"][b][c]", match_anywhere=False, match_children=True)
  assert isinstance(sel, Selector_Element)
  assert sel.tag == "a"

  assert isinstance(sel.attribute_selectors, list)
  assert len(sel.attribute_selectors) == 3

  assert isinstance(sel.attribute_selectors[0], AttributeSelector_Equal)
  assert sel.attribute_selectors[0].name == "a"
  assert sel.attribute_selectors[0].value == "1"

  assert isinstance(sel.attribute_selectors[1], AttributeSelector_HasName)
  assert sel.attribute_selectors[1].name == "b"

  assert isinstance(sel.attribute_selectors[2], AttributeSelector_HasName)
  assert sel.attribute_selectors[2].name == "c"

  #...

  sel = selector.parse_selector("a b", match_anywhere=False, match_children=True)
  assert isinstance(sel, Selector_Children)

  assert isinstance(sel.cur_selector, Selector_Element)
  assert sel.cur_selector.tag == "a"
  assert sel.cur_selector.attribute_selectors == []

  assert isinstance(sel.next_selector, Selector_Element)
  assert sel.next_selector.tag == "b"
  assert sel.next_selector.attribute_selectors == []

  #...

  sel = selector.parse_selector("a > b", match_anywhere=False, match_children=True)
  assert isinstance(sel, Selector_Son)

  assert isinstance(sel.cur_selector, Selector_Element)
  assert sel.cur_selector.tag == "a"
  assert sel.cur_selector.attribute_selectors == []

  assert isinstance(sel.next_selector, Selector_Element)
  assert sel.next_selector.tag == "b"
  assert sel.next_selector.attribute_selectors == []

  #...

  sel = selector.parse_selector("  abc  ", match_anywhere=False, match_children=True)
  assert isinstance(sel, Selector_Element)
  assert sel.tag == "abc"
  assert sel.attribute_selectors == []
