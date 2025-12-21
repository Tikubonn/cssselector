
import string
from abc import ABC, abstractmethod
from typing import Self
from dataclasses import dataclass
from .exception import ParseError
from .attribute_selector import IAttributeSelector, AttributeSelector_Equal, AttributeSelector_ContainsWithSeparator, parse_attribute_selector

class ISelector (ABC):

  """セレクターを表現するインターフェイスです。"""

  @abstractmethod
  def match (self, element_stack:list[tuple[str, dict[str, str]]], index:int=0) -> bool:

    """HTMLの階層に見立てたスタックが自身の条件に一致するかを判定します。

    Parameters
    ----------
    element_stack : list[tuple[str, dict[str, str]]]
      HTMLの階層に見立てたスタックです。
      これはタグ名・属性の辞書のリストで表現されます。
    index : int
      判定を開始する階層の位置です。
      未指定ならば `0` が設定されます。

    Returns
    -------
    bool
      スタックが条件に一致したならば `True` そうでなければ `False` を返します。
    """

    pass

class IGeneratableFromStack (ABC):

  """スタックから自身を作成する規格を提供します。

  Notes
  -----
  本インターフェイスは `parse_selector` 関数内で結合子による木構造を構築する際に使われます。
  """

  @classmethod
  @abstractmethod
  def from_stack (cls, selector_stack:list[ISelector]) -> Self:

    """セレクターのスタックから自身のインスタンスを作成します。

    Parameters
    ----------
    selector_stack : list[ISelector]
      自身を作成するために参照される `ISelector` が詰め込まれたスタックです。
      このスタックはインスタンスの作成過程で変更操作が行われる可能性があります。

    Returns
    -------
    Self
      作成された自身のインスタンスです。
    """

    pass

@dataclass
class Selector_Element (ISelector):

  """複合セレクターを表現します。

  Parameters
  ----------
  tag : str
    一致させるタグ名です。
    空文字列が指定されたならば全てのタグ名に一致します。
  attribute_selectors : list[IAttributeSelector]
    一致させる属性セレクターのリストです。
  """

  tag:str
  attribute_selectors:list[IAttributeSelector]

  def match (self, element_stack:list[tuple[str, dict[str, str]]], index:int=0) -> bool:
    if index < len(element_stack):
      tag, attributes = element_stack[index]
      return (not self.tag or self.tag == tag) and all((sel.match(attributes) for sel in self.attribute_selectors))
    else:
      return False

@dataclass
class Selector_Children (ISelector, IGeneratableFromStack):

  """子孫結合子を表現します。

  Parameters
  ----------
  cur_selector : ISelector
    親要素を表すセレクターです。
  next_selector : ISelector
    子要素を表すセレクターです。
  """

  cur_selector:ISelector
  next_selector:ISelector

  def match (self, element_stack:list[tuple[str, dict[str, str]]], index:int=0) -> bool:
    return self.cur_selector.match(element_stack, index) and any((self.next_selector.match(element_stack, i) for i in range(index +1, len(element_stack))))

  @classmethod
  def from_stack (cls, selector_stack:list[ISelector]) -> Self:
    next_selector = selector_stack.pop()
    cur_selector = selector_stack.pop()
    return cls(cur_selector, next_selector)

@dataclass
class Selector_Son (ISelector, IGeneratableFromStack):

  """子結合子を表現します。

  Parameters
  ----------
  cur_selector : ISelector
    親要素を表すセレクターです。
  next_selector : ISelector
    子要素を表すセレクターです。
  """

  cur_selector:ISelector
  next_selector:ISelector

  def match (self, element_stack:list[tuple[str, dict[str, str]]], index:int=0) -> bool:
    return self.cur_selector.match(element_stack, index) and self.next_selector.match(element_stack, index +1)

  @classmethod
  def from_stack (cls, selector_stack:list[ISelector]) -> Self:
    next_selector = selector_stack.pop()
    cur_selector = selector_stack.pop()
    return cls(cur_selector, next_selector)

@dataclass
class Selector_MatchAnywhere (ISelector, IGeneratableFromStack):

  """指定セレクターが一致するまで、あらゆる位置で一致判定を試行します。

  Parameters
  ----------
  selector : ISelector
    一致を試みるセレクターです。
  """

  selector:ISelector

  def match (self, element_stack:list[tuple[str, dict[str, str]]], index:int=0) -> bool:
    return any((self.selector.match(element_stack, i) for i in range(len(element_stack))))

  @classmethod
  def from_stack (cls, selector_stack:list[ISelector]) -> Self:
    selector = selector_stack.pop()
    return cls(selector)

@dataclass
class Selector_MatchLast (ISelector, IGeneratableFromStack):

  """指定セレクターが最下層で一致するかを判定します。

  Parameters
  ----------
  selector : ISelector
    一致を試みるセレクターです。
  """

  selector:ISelector

  def match (self, element_stack:list[tuple[str, dict[str, str]]], index:int=0) -> bool:
    return index +1 == len(element_stack) and self.selector.match(element_stack, index)

  @classmethod
  def from_stack (cls, selector_stack:list[ISelector]) -> Self:
    selector = selector_stack.pop()
    return cls(selector)

#parser

TAG_CHARS:set[str] = set(string.ascii_letters + string.digits + "-_")
TAG_START_CHARS:set[str] = set(string.ascii_letters)

def _read_tag (source:str, start:int, end:int) -> tuple[str, int]:
  if start < end:
    if source[start] == "*":
      return "", start +1
    elif source[start] in TAG_START_CHARS:
      tmp = source[start]
      index = start +1
      while index < end and source[index] in TAG_CHARS:
        tmp += source[index]
        index += 1
      return tmp, index
    else:
      return "", start
  else:
    raise ParseError.at("Reached end of data on parsing.", (source, start))

CLASS_AND_ID_CHARS:set[str] = set(string.ascii_letters + string.digits + "-_")
CLASS_AND_ID_START_CHARS:set[str] = set(string.ascii_letters)

def _read_class_and_id (source:str, start:int, end:int) -> tuple[str, int]:
  if start < end:
    if source[start] in CLASS_AND_ID_START_CHARS:
      tmp = source[start]
      index = start +1
      while index < end and source[index] in CLASS_AND_ID_CHARS:
        tmp += source[index]
        index += 1
      return tmp, index
    else:
      raise ParseError.at("Read an invalid character to start of class, id identifier: {:s}".format(repr(source[start])), (source, start))
  else:
    raise ParseError.at("Reached end of data on parsing.", (source, start))

SEPARATOR_CHARS:set[str] = set("> ")

def _read_separator (source:str, start:int, end:int) -> tuple[str, int]:
  tmp = ""
  index = start
  while index < end and source[index] in SEPARATOR_CHARS:
    tmp += source[index]
    index += 1
  return tmp, index

def _strip (source:str) -> tuple[int, int]:
  start = 0
  index = 0
  while index < len(source):
    if source[index] == " ":
      start = index +1
      index += 1
    else:
      break
  end = len(source)
  index = 0
  while index < len(source):
    rindex = len(source) - (index +1)
    if source[rindex] == " ":
      end = rindex
      index += 1
    else:
      break
  return start, end

def parse_selector (source:str, *, match_anywhere:bool=True, match_children:bool=True) -> ISelector:

  """セレクターのコードをパースします。

  Parameters
  ----------
  source : str
    パースするコードが記述された文字列です。
  match_anywhere : bool
    パースされた `ISelector` インスタンスが任意の位置で一致させるかを設定します。
  match_children : bool
    パースされた `ISelector` インスタンスが一致した要素の子孫に対しても一致させるかを設定します。

  Returns
  -------
  ISelector
    パースされた `ISelector` インスタンスです。
  """

  selector_stack = []
  rel_selector_type_stack = []

  #parse source.

  start, end = _strip(source)
  index = start
  while index < end:
    tag, index = _read_tag(source, index, end)
    attribute_selectors = []
    while index < end:
      if source[index:].startswith("."):
        class_, index = _read_class_and_id(source, index +1, end)
        sel = AttributeSelector_ContainsWithSeparator("class", class_)
        attribute_selectors.append(sel)
      elif source[index:].startswith("#"):
        id_, index = _read_class_and_id(source, index +1, end)
        sel = AttributeSelector_Equal("id", id_)
        attribute_selectors.append(sel)
      elif source[index:].startswith("["):
        sel, index = parse_attribute_selector(source, index, end)
        attribute_selectors.append(sel)
      else:
        break
    sel = Selector_Element(tag, attribute_selectors)
    selector_stack.append(sel)
    if index < end:
      separator, index = _read_separator(source, index, end)
      match separator.strip():
        case "":
          rel_selector_type_stack.append(Selector_Children)
        case ">":
          rel_selector_type_stack.append(Selector_Son)
        case _:
          raise ParseError.at("Read unknown separator: {:s}".format(repr(separator)), (source, index))
    else:
      break

  #build selector tree.

  if match_anywhere:
    rel_selector_type_stack.insert(0, Selector_MatchAnywhere)
  if not match_children:
    rel_selector_type_stack.append(Selector_MatchLast)
  if selector_stack:
    while rel_selector_type_stack:
      rel_selector_type = rel_selector_type_stack.pop()
      sel = rel_selector_type.from_stack(selector_stack)
      selector_stack.append(sel)
    sel = selector_stack[-1]
    return sel
  else:
    raise ParseError.at("Could not read any selector even one.", (source, index))
