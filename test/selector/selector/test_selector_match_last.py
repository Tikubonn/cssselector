
import pytest
from cssselector import Selector_Element, Selector_MatchLast

def test_selector_match_last ():

  sel = Selector_MatchLast()

  #...

  assert sel.match([("a", {}), ("b", {})], match_children=True) == True
  assert sel.match([("a", {})], match_children=True) == True
  assert sel.match([], match_children=True) == True

  #...

  assert sel.match([("a", {}), ("b", {})], match_children=False) == False
  assert sel.match([("a", {})], match_children=False) == False
  assert sel.match([], match_children=False) == True
