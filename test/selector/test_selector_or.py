
import pytest
from cssselector import Selector_Or, Selector_Element

def test_selector_or ():
  sel = Selector_Or([
    Selector_Element("a", []),
    Selector_Element("b", []),
    Selector_Element("c", []),
  ])
  assert sel.match([("a", {})]) == True
  assert sel.match([("b", {})]) == True
  assert sel.match([("c", {})]) == True
  assert sel.match([("x", {})]) == False
  assert sel.match([]) == False
