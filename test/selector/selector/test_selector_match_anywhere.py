
import pytest
from cssselector import Selector_Element, Selector_MatchAnywhere

def test_selector_match_anywhere ():

  sel = Selector_MatchAnywhere(
    Selector_Element("a", {}))

  #...

  assert sel.match([("x", {}), ("x", {}), ("a", {})], match_anywhere=True) == True
  assert sel.match([("x", {}), ("a", {})], match_anywhere=True) == True
  assert sel.match([("a", {})], match_anywhere=True) == True
  assert sel.match([], match_anywhere=True) == False

  #...

  assert sel.match([("x", {}), ("x", {}), ("a", {})], match_anywhere=False) == False
  assert sel.match([("x", {}), ("a", {})], match_anywhere=False) == False
  assert sel.match([("a", {})], match_anywhere=False) == True
  assert sel.match([], match_anywhere=False) == False
