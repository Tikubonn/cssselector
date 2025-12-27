
import pytest
from cssselector import AttributeSelector_Equal, Selector_Element, Element

def test_selector_element ():

  sel = Selector_Element("a", [])
  assert sel.match([("a", {}), ("b", {})]) == True
  assert sel.match([("a", {})]) == True
  assert sel.match([]) == False

  sel = Selector_Element("a", [AttributeSelector_Equal("a", "1")])
  assert sel.match([("a", {"a": "1", "b": "2"})]) == True
  assert sel.match([("a", {"a": "1"})]) == True
  assert sel.match([("a", {})]) == False
  assert sel.match([]) == False
