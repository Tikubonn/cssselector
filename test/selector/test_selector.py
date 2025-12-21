
import pytest
from cssselector import Selector_Element, Selector_Children, Selector_Son, Selector_MatchAnywhere, Selector_MatchLast, AttributeSelector_Equal

def test_selector_element ():

  #...

  sel = Selector_Element("a", [])
  assert sel.match([("a", {}), ("b", {})]) == True
  assert sel.match([("a", {})]) == True
  assert sel.match([]) == False
  
  #...

  sel = Selector_Element("a", [AttributeSelector_Equal("a", "1")])
  assert sel.match([("a", {"a": "1", "b": "2"})]) == True
  assert sel.match([("a", {"a": "1"})]) == True
  assert sel.match([("a", {})]) == False
  assert sel.match([]) == False

def test_selector_children ():
  sel = Selector_Children(
    Selector_Element("a", {}), 
    Selector_Element("b", {}))
  assert sel.match([("a", {}), ("x", {}), ("b", {})]) == True
  assert sel.match([("a", {}), ("b", {})]) == True
  assert sel.match([("a", {})]) == False
  assert sel.match([]) == False

def test_selector_son ():
  sel = Selector_Son(
    Selector_Element("a", {}), 
    Selector_Element("b", {}))
  assert sel.match([("a", {}), ("x", {}), ("b", {})]) == False
  assert sel.match([("a", {}), ("b", {})]) == True
  assert sel.match([("a", {})]) == False
  assert sel.match([]) == False

def test_selector_match_anywhere ():
  sel = Selector_MatchAnywhere(
    Selector_Element("a", {}))
  assert sel.match([("x", {}), ("x", {}), ("a", {})]) == True
  assert sel.match([("x", {}), ("a", {})]) == True
  assert sel.match([("a", {})]) == True
  assert sel.match([]) == False

def test_selector_match_last ():
  sel = Selector_MatchLast(
    Selector_Element("a", {}))
  assert sel.match([("a", {}), ("b", {})]) == False
  assert sel.match([("a", {})]) == True
  assert sel.match([]) == False
