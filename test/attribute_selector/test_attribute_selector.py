
import pytest
from cssselector import AttributeSelector_HasName, AttributeSelector_Equal, AttributeSelector_StartsWith, AttributeSelector_EndsWith, AttributeSelector_ContainsAnywhere, AttributeSelector_ContainsWithSeparator

def test_attribute_selector_has_name ():
  sel = AttributeSelector_HasName("a")
  assert sel.match({"a": "1", "b": "2"}) == True
  assert sel.match({"a": "1"}) == True
  assert sel.match({}) == False

def test_attribute_selector_equal ():
  sel = AttributeSelector_Equal("a", "1")
  assert sel.match({"a": "1", "b": "2"}) == True
  assert sel.match({"a": "1"}) == True
  assert sel.match({}) == False
  assert sel.match({"a": "3", "b": "2"}) == False
  assert sel.match({"a": "3"}) == False
  assert sel.match({}) == False

def test_attribute_selector_starts_with ():
  sel = AttributeSelector_StartsWith("a", "1")
  assert sel.match({"a": "123", "b": "2"}) == True
  assert sel.match({"a": "123"}) == True
  assert sel.match({}) == False
  assert sel.match({"a": "321", "b": "2"}) == False
  assert sel.match({"a": "321"}) == False
  assert sel.match({}) == False

def test_attribute_selector_ends_with ():
  sel = AttributeSelector_EndsWith("a", "3")
  assert sel.match({"a": "123", "b": "2"}) == True
  assert sel.match({"a": "123"}) == True
  assert sel.match({}) == False
  assert sel.match({"a": "321", "b": "2"}) == False
  assert sel.match({"a": "321"}) == False
  assert sel.match({}) == False

def test_attribute_selector_contains_anywhere ():
  sel = AttributeSelector_ContainsAnywhere("a", "2")
  assert sel.match({"a": "123", "b": "2"}) == True
  assert sel.match({"a": "123"}) == True
  assert sel.match({}) == False
  assert sel.match({"a": "3x1", "b": "2"}) == False
  assert sel.match({"a": "3x1"}) == False
  assert sel.match({}) == False

def test_attribute_selector_contains_with_separator ():
  sel = AttributeSelector_ContainsWithSeparator("a", "2")
  assert sel.match({"a": "1 2 3", "b": "2"}) == True
  assert sel.match({"a": "1 2 3"}) == True
  assert sel.match({}) == False
  assert sel.match({"a": "1 x 3", "b": "2"}) == False
  assert sel.match({"a": "1 x 3"}) == False
  assert sel.match({}) == False
