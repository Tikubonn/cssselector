
import pytest
from cssselector import selector, ParseError, Selector_Element, Selector_Children, Selector_Son, Selector_MatchAnywhere, Selector_MatchLast, AttributeSelector_HasName, AttributeSelector_Equal, Selector_Or, AttributeSelector_ContainsWithSeparator

def test_read_tag ():

  #非公開関数 _read_tag の動作確認を行います

  #文字列 "*" を読み込んだ場合の動作確認です

  tag, index = selector._read_tag("*", 0, 1)
  assert tag == ""
  assert index == 1

  #任意の有効な文字列を読み込んだ場合の動作確認です

  tag, index = selector._read_tag("abc def", 0, 7)
  assert tag == "abc"
  assert index == 3

  #任意の無効な文字列を読み込んだ場合の動作確認です

  tag, index = selector._read_tag(".abc", 0, 5)
  assert tag == ""
  assert index == 0

  tag, index = selector._read_tag("#abc", 0, 5)
  assert tag == ""
  assert index == 0

  tag, index = selector._read_tag("[abc]", 0, 5)
  assert tag == ""
  assert index == 0

  #空文字列を読み込んだ場合に例外が発生するかを検証します

  with pytest.raises(ParseError):
    selector._read_tag("", 0, 0)

def test_read_class_and_id ():

  #非公開関数 _read_class_and_id の動作を検証します

  #任意の有効な文字列を読み込んだ場合の動作確認です

  identifier, index = selector._read_tag("abc def", 0, 7)
  assert identifier == "abc"
  assert index == 3

  #空文字列を読み込んだ場合に例外が発生するかを検証します

  with pytest.raises(ParseError):
    selector._read_class_and_id("", 0, 0)

  #１文字目が無効な文字の場合に例外が発生するかを検証します

  with pytest.raises(ParseError):
    selector._read_class_and_id(" ", 0, 1)

def test_read_separator ():

  #非公開関数 _read_separator の動作を検証します

  #空白文字のみの文字列の場合の動作確認です

  separator, index = selector._read_separator("  ", 0, 2)
  assert separator == "  "
  assert index == 2

  #空白文字と ">" を含んだ文字列の場合の動作確認です

  separator, index = selector._read_separator(" > ", 0, 3)
  assert separator == " > "
  assert index == 3

  #空白文字と "," を含んだ文字列の場合の動作確認です

  separator, index = selector._read_separator(" , ", 0, 3)
  assert separator == " , "
  assert index == 3

  #区切り文字を含まない場合の動作確認です

  separator, index = selector._read_separator("abc", 0, 3)
  assert separator == ""
  assert index == 0

  #前方に区切り文字を含む場合の動作確認です

  separator, index = selector._read_separator("  abc", 0, 3)
  assert separator == "  "
  assert index == 2

  #後方に区切り文字を含む場合の動作確認です

  separator, index = selector._read_separator("abc  ", 0, 3)
  assert separator == ""
  assert index == 0

  #前後に区切り文字を含む場合の動作確認です

  separator, index = selector._read_separator("  abc  ", 0, 3)
  assert separator == "  "
  assert index == 2

def test_strip ():

  #_strip 関数の動作確認です

  #前後に空白文字がない場合の動作確認です

  start, end = selector._strip("abc")
  assert start == 0
  assert end == 3

  #前方に空白文字を含む場合の動作確認です

  start, end = selector._strip("  abc")
  assert start == 2
  assert end == 5

  #後方に空白文字を含む場合の動作確認です

  start, end = selector._strip("abc  ")
  assert start == 0
  assert end == 3

  #前後に空白文字を含む場合の動作確認です

  start, end = selector._strip("  abc  ")
  assert start == 2
  assert end == 5

  #空文字列を読み込んだ場合の動作確認です

  start, end = selector._strip("")
  assert start == 0
  assert end == 0

def test_build ():

  #非公開関数 _build の動作確認を行います 

  #空リストを読み込んだ場合に例外が発生するかを検証します

  with pytest.raises(ParseError):
    selector._build([], [], ("", 0))

  #read_selector_stack のみに値を設定した場合の動作確認です

  sel = selector._build([Selector_Element("a", [])], [], ("", 0))
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_MatchLast)

  #read_selector_stack, combination_selector_type_stack 両方に値を設定した場合の動作確認です

  sel = selector._build([Selector_Element("a", []), Selector_Element("b", [])], [Selector_Children], ("", 0))
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Children)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_Son)
  assert isinstance(sel.selector.next_selector.cur_selector, Selector_Element)
  assert sel.selector.next_selector.cur_selector.tag == "b"
  assert sel.selector.next_selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector.next_selector, Selector_MatchLast)

def test_parse_selector ():

  #...

  with pytest.raises(ParseError):
    selector.parse_selector("")

  #...

  sel = selector.parse_selector("a")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_MatchLast)

  #...

  sel = selector.parse_selector("a.abc")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert isinstance(sel.selector.cur_selector.attribute_selectors, list)
  assert len(sel.selector.cur_selector.attribute_selectors) == 1
  assert isinstance(sel.selector.cur_selector.attribute_selectors[0], AttributeSelector_ContainsWithSeparator)
  assert sel.selector.cur_selector.attribute_selectors[0].name == "class"
  assert sel.selector.cur_selector.attribute_selectors[0].value == "abc"

  #...

  sel = selector.parse_selector("a#abc")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert isinstance(sel.selector.cur_selector.attribute_selectors, list)
  assert len(sel.selector.cur_selector.attribute_selectors) == 1
  assert isinstance(sel.selector.cur_selector.attribute_selectors[0], AttributeSelector_Equal)
  assert sel.selector.cur_selector.attribute_selectors[0].name == "id"
  assert sel.selector.cur_selector.attribute_selectors[0].value == "abc"

  #...

  sel = selector.parse_selector("a[a=\"1\"][b][c]")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert isinstance(sel.selector.cur_selector.attribute_selectors, list)
  assert len(sel.selector.cur_selector.attribute_selectors) == 3
  assert isinstance(sel.selector.cur_selector.attribute_selectors[0], AttributeSelector_Equal)
  assert sel.selector.cur_selector.attribute_selectors[0].name == "a"
  assert sel.selector.cur_selector.attribute_selectors[0].value == "1"
  assert isinstance(sel.selector.cur_selector.attribute_selectors[1], AttributeSelector_HasName)
  assert sel.selector.cur_selector.attribute_selectors[1].name == "b"
  assert isinstance(sel.selector.cur_selector.attribute_selectors[2], AttributeSelector_HasName)
  assert sel.selector.cur_selector.attribute_selectors[2].name == "c"

  #...

  sel = selector.parse_selector("a b")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Children)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_Son)
  assert isinstance(sel.selector.next_selector.cur_selector, Selector_Element)
  assert sel.selector.next_selector.cur_selector.tag == "b"
  assert sel.selector.next_selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector.next_selector, Selector_MatchLast)

  #...

  sel = selector.parse_selector("a > b")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "a"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_Son)
  assert isinstance(sel.selector.next_selector.cur_selector, Selector_Element)
  assert sel.selector.next_selector.cur_selector.tag == "b"
  assert sel.selector.next_selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector.next_selector, Selector_MatchLast)

  #...

  sel = selector.parse_selector("  abc  ")
  assert isinstance(sel, Selector_MatchAnywhere)
  assert isinstance(sel.selector, Selector_Son)
  assert isinstance(sel.selector.cur_selector, Selector_Element)
  assert sel.selector.cur_selector.tag == "abc"
  assert sel.selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selector.next_selector, Selector_MatchLast)

  #...

  sel = selector.parse_selector("a,b,c")
  assert isinstance(sel, Selector_Or)
  assert isinstance(sel.selectors, list)
  assert len(sel.selectors) == 3
  assert isinstance(sel.selectors[0], Selector_MatchAnywhere)
  assert isinstance(sel.selectors[0].selector, Selector_Son)
  assert isinstance(sel.selectors[0].selector.cur_selector, Selector_Element)
  assert sel.selectors[0].selector.cur_selector.tag == "a"
  assert sel.selectors[0].selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selectors[1], Selector_MatchAnywhere)
  assert isinstance(sel.selectors[1].selector, Selector_Son)
  assert isinstance(sel.selectors[1].selector.cur_selector, Selector_Element)
  assert sel.selectors[1].selector.cur_selector.tag == "b"
  assert sel.selectors[1].selector.cur_selector.attribute_selectors == []
  assert isinstance(sel.selectors[2], Selector_MatchAnywhere)
  assert isinstance(sel.selectors[2].selector, Selector_Son)
  assert isinstance(sel.selectors[2].selector.cur_selector, Selector_Element)
  assert sel.selectors[2].selector.cur_selector.tag == "c"
  assert sel.selectors[2].selector.cur_selector.attribute_selectors == []
