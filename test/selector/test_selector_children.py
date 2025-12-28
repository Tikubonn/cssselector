
import pytest
from cssselector import Selector_Element, Selector_Children

def test_selector_children ():
  sel = Selector_Children(
    Selector_Element("a", {}), 
    Selector_Element("b", {}))
  assert sel.match([("a", {}), ("x", {}), ("b", {})]) == True
  assert sel.match([("a", {}), ("b", {})]) == True
  assert sel.match([("a", {})]) == False
  assert sel.match([]) == False
