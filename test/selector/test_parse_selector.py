
import pytest
from cssselector import selector, ParseError, Selector_Element, Selector_Children, Selector_Son, Selector_MatchAnywhere, Selector_MatchLast, AttributeSelector_HasName, AttributeSelector_Equal, Selector_Or, AttributeSelector_ContainsWithSeparator

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

  sel = selector.parse_selector("a")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_MatchLast)

  #...

  sel = selector.parse_selector("a.abc")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert isinstance(sel.selector.cur_selector.attribute_selectors, list)
  assert len(sel.selector.cur_selector.attribute_selectors) == 1
  assert isinstance(sel.selector.cur_selector.attribute_selectors[0], AttributeSelector_ContainsWithSeparator)
  assert sel.selector.cur_selector.attribute_selectors[0].name == "class"
  assert sel.selector.cur_selector.attribute_selectors[0].value == "abc"

  #...

  sel = selector.parse_selector("a#abc")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert isinstance(sel.selector.cur_selector.attribute_selectors, list)
  assert len(sel.selector.cur_selector.attribute_selectors) == 1
  assert isinstance(sel.selector.cur_selector.attribute_selectors[0], AttributeSelector_Equal)
  assert sel.selector.cur_selector.attribute_selectors[0].name == "id"
  assert sel.selector.cur_selector.attribute_selectors[0].value == "abc"

  #...

  sel = selector.parse_selector("a[a=\"1\"][b][c]")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert isinstance(sel.selector.cur_selector.attribute_selectors, list)
  assert len(sel.selector.cur_selector.attribute_selectors) == 3
  assert isinstance(sel.selector.cur_selector.attribute_selectors[0], AttributeSelector_Equal)
  assert sel.selector.cur_selector.attribute_selectors[0].name == "a"
  assert sel.selector.cur_selector.attribute_selectors[0].value == "1"
  assert isinstance(sel.selector.cur_selector.attribute_selectors[1], AttributeSelector_HasName)
  assert sel.selector.cur_selector.attribute_selectors[1].name == "b"
  assert isinstance(sel.selector.cur_selector.attribute_selectors[2], AttributeSelector_HasName)
  assert sel.selector.cur_selector.attribute_selectors[2].name == "c"

  #...

  sel = selector.parse_selector("a b")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Children)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_Son)
  assert isinstance(sel.selector.next_selector.cur_selector, Selector_Element)
  assert sel.selector.next_selector.cur_selector.tag == "b"
  assert sel.selector.next_selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector.next_selector, Selector_MatchLast)

  #...

  sel = selector.parse_selector("a > b")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_Son)
  assert isinstance(sel.selector.next_selector.cur_selector, Selector_Element)
  assert sel.selector.next_selector.cur_selector.tag == "b"
  assert sel.selector.next_selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector.next_selector, Selector_MatchLast)

  #...

  sel = selector.parse_selector("  abc  ")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "abc"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_MatchLast)

  #...

  sel = selector.parse_selector("a,b,c")
  assert isinstance(sel, Selector_Or)
  assert isinstance(sel.selectors, list)
  assert len(sel.selectors) == 3
  assert isinstance(sel.selectors[0], Selector_MatchAnywhere)
  assert isinstance(sel.selectors[0].selector, Selector_Son)
  assert isinstance(sel.selectors[0].selector.cur_selector, Selector_Element)
  assert sel.selectors[0].selector.cur_selector.tag == "a"
  assert sel.selectors[0].selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selectors[1], Selector_MatchAnywhere)
  assert isinstance(sel.selectors[1].selector, Selector_Son)
  assert isinstance(sel.selectors[1].selector.cur_selector, Selector_Element)
  assert sel.selectors[1].selector.cur_selector.tag == "b"
  assert sel.selectors[1].selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selectors[2], Selector_MatchAnywhere)
  assert isinstance(sel.selectors[2].selector, Selector_Son)
  assert isinstance(sel.selectors[2].selector.cur_selector, Selector_Element)
  assert sel.selectors[2].selector.cur_selector.tag == "c"
  assert sel.selectors[2].selector.cur_selector.attribute_selectors == []
