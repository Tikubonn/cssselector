
import pytest
from cssselector import Selector_Element, Selector_Son

def test_selector_son ():
  sel = Selector_Son(
    Selector_Element("a", {}), 
    Selector_Element("b", {}))
  assert sel.match([("a", {}), ("x", {}), ("b", {})]) == False
  assert sel.match([("a", {}), ("b", {})]) == True
  assert sel.match([("a", {})]) == False
  assert sel.match([]) == False
