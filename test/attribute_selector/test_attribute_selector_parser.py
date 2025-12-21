
import pytest
from cssselector import attribute_selector, ParseError, AttributeSelector_HasName, AttributeSelector_Equal, AttributeSelector_StartsWith, AttributeSelector_EndsWith, AttributeSelector_ContainsAnywhere, AttributeSelector_ContainsWithSeparator

def test_read_attribute_name ():

  #...

  with pytest.raises(ParseError):
    attribute_selector._read_attribute_name("", 0, 0)

  #...

  with pytest.raises(ParseError):
    attribute_selector._read_attribute_name("-", 0, 1)

  #...

  name, index = attribute_selector._read_attribute_name("abc", 0, 3)
  assert name == "abc"
  assert index == 3

  name, index = attribute_selector._read_attribute_name("abc=", 0, 4)
  assert name == "abc"
  assert index == 3

def test_read_attribute_value ():

  #...

  with pytest.raises(ParseError):
    attribute_selector._read_attribute_value("", 0, 0)

  #...

  with pytest.raises(ParseError):
    attribute_selector._read_attribute_value("abc", 0, 3)

  #...

  with pytest.raises(ParseError):
    attribute_selector._read_attribute_value("\"abc", 0, 4)

  #...

  with pytest.raises(ParseError):
    attribute_selector._read_attribute_value("\"abc\"", 0, 5)

  #...

  value, index = attribute_selector._read_attribute_value("\"abc\"]", 0, 6)
  assert value == "abc"
  assert index == 6

  #...

  value, index = attribute_selector._read_attribute_value("\"&lt;\"]", 0, 7)
  assert value == "<"
  assert index == 7

def test_parse_attribute_selector ():

  #...

  with pytest.raises(ParseError):
    attribute_selector.parse_attribute_selector("", 0, 0)

  #...

  with pytest.raises(ParseError):
    attribute_selector.parse_attribute_selector("abc", 0, 3)

  #...

  with pytest.raises(ParseError):
    attribute_selector.parse_attribute_selector("[a b]", 0, 5)

  #...

  selector, index = attribute_selector.parse_attribute_selector("[a]", 0, 3)
  assert isinstance(selector, AttributeSelector_HasName) == True
  assert selector.name == "a"
  assert index == 3

  #...

  selector, index = attribute_selector.parse_attribute_selector("[a=\"b\"]", 0, 7)
  assert isinstance(selector, AttributeSelector_Equal) == True
  assert selector.name == "a"
  assert selector.value == "b"
  assert index == 7

  #...

  selector, index = attribute_selector.parse_attribute_selector("[a^=\"b\"]", 0, 8)
  assert isinstance(selector, AttributeSelector_StartsWith) == True
  assert selector.name == "a"
  assert selector.value == "b"
  assert index == 8

  #...

  selector, index = attribute_selector.parse_attribute_selector("[a$=\"b\"]", 0, 8)
  assert isinstance(selector, AttributeSelector_EndsWith) == True
  assert selector.name == "a"
  assert selector.value == "b"
  assert index == 8

  #...

  selector, index = attribute_selector.parse_attribute_selector("[a*=\"b\"]", 0, 8)
  assert isinstance(selector, AttributeSelector_ContainsAnywhere) == True
  assert selector.name == "a"
  assert selector.value == "b"
  assert index == 8

  #...

  selector, index = attribute_selector.parse_attribute_selector("[a~=\"b\"]", 0, 8)
  assert isinstance(selector, AttributeSelector_ContainsWithSeparator) == True
  assert selector.name == "a"
  assert selector.value == "b"
  assert index == 8
