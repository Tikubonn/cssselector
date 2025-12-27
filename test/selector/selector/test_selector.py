
import pytest
from cssselector import Selector_Element, Selector_Son, Selector_MatchAnywhere, Selector_MatchLast

def test_selector ():

  #複数のセレクターを組み合わせた挙動を検証します。

  sel = Selector_MatchAnywhere(
    Selector_Son(
      Selector_Element("a", []),
      Selector_MatchLast()))

  #...

  assert sel.match([("x", []), ("a", []), ("x", [])], match_anywhere=True, match_children=True) == True
  assert sel.match([("a", []), ("x", [])], match_anywhere=True, match_children=True) == True
  assert sel.match([("x", [])], match_anywhere=True, match_children=True) == False
  assert sel.match([], match_anywhere=True, match_children=True) == False

  #...

  assert sel.match([("x", []), ("a", []), ("x", [])], match_anywhere=False, match_children=True) == False
  assert sel.match([("a", []), ("x", [])], match_anywhere=False, match_children=True) == True
  assert sel.match([("x", [])], match_anywhere=False, match_children=True) == False
  assert sel.match([], match_anywhere=False, match_children=True) == False

  #...

  assert sel.match([("x", []), ("a", []), ("x", [])], match_anywhere=True, match_children=False) == False
  assert sel.match([("x", []), ("a", [])], match_anywhere=True, match_children=False) == True
  assert sel.match([("x", [])], match_anywhere=True, match_children=False) == False
  assert sel.match([], match_anywhere=True, match_children=False) == False

  #...

  assert sel.match([("a", []), ("x", []), ("x", [])], match_anywhere=False, match_children=False) == False
  assert sel.match([("a", []), ("x", [])], match_anywhere=False, match_children=False) == False
  assert sel.match([("a", [])], match_anywhere=False, match_children=False) == True
  assert sel.match([], match_anywhere=False, match_children=False) == False
