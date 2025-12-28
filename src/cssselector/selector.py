
import string
from abc import ABC, abstractmethod
from typing import NamedTuple, Self, Type
from dataclasses import dataclass
from .exception import ParseError
from .attribute_selector import IAttributeSelector, AttributeSelector_Equal, AttributeSelector_ContainsWithSeparator, parse_attribute_selector

class Element (NamedTuple):

  """HTML要素を表現するクラスです。

  Attributes
  ----------
  tag : str
    要素名です。
  attrs : dict[str, str]
    要素に設定された属性の集合です。
  """

  tag:str
  attrs:dict[str, str]

class ISelector (ABC):

  """セレクターを表現するインターフェイスです。"""

  @abstractmethod
  def match (self, element_stack:list[Element], index:int=0, *, match_anywhere:bool=True, match_children:bool=False) -> bool:

    """HTMLの階層に見立てたスタックが自身の条件に一致するかを判定します。

    Parameters
    ----------
    element_stack : list[Element]
      HTMLの階層に見立てたスタックです。
      これはタグ名・属性の辞書のリストで表現されます。
    index : int
      判定を開始する階層の位置です。
      未指定ならば `0` が設定されます。
    match_anywhere : bool
      任意の位置での一致を許可するかを指定します。
    match_children : bool
      一致した要素の子孫に対しても一致したものとして扱うかを指定します。

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

  Attributes
  ----------
  tag : str
    一致させるタグ名です。
    空文字列が指定されたならば全てのタグ名に一致します。
  attribute_selectors : list[IAttributeSelector]
    一致させる属性セレクターのリストです。
  """

  tag:str
  attribute_selectors:list[IAttributeSelector]

  def match (self, element_stack:list[Element], index:int=0, *, match_anywhere:bool=True, match_children:bool=False) -> bool:
    if index < len(element_stack):
      tag, attributes = element_stack[index]
      return (
        (not self.tag or self.tag == tag) and 
        all((sel.match(attributes) for sel in self.attribute_selectors))
      )
    else:
      return False

@dataclass
class Selector_Children (ISelector, IGeneratableFromStack):

  """子孫結合子を表現します。

  Attributes
  ----------
  cur_selector : ISelector
    親要素を表すセレクターです。
  next_selector : ISelector
    子要素を表すセレクターです。
  """

  cur_selector:ISelector
  next_selector:ISelector

  def match (self, element_stack:list[Element], index:int=0, *, match_anywhere:bool=True, match_children:bool=False) -> bool:
    return (
      self.cur_selector.match(element_stack, index, match_anywhere=match_anywhere, match_children=match_children) and 
      any((self.next_selector.match(element_stack, i, match_anywhere=match_anywhere, match_children=match_children) for i in range(index +1, len(element_stack))))
    )

  @classmethod
  def from_stack (cls, selector_stack:list[ISelector]) -> Self:
    next_selector = selector_stack.pop()
    cur_selector = selector_stack.pop()
    return cls(cur_selector, next_selector)

@dataclass
class Selector_Son (ISelector, IGeneratableFromStack):

  """子結合子を表現します。

  Attributes
  ----------
  cur_selector : ISelector
    親要素を表すセレクターです。
  next_selector : ISelector
    子要素を表すセレクターです。
  """

  cur_selector:ISelector
  next_selector:ISelector

  def match (self, element_stack:list[Element], index:int=0, *, match_anywhere:bool=True, match_children:bool=False) -> bool:
    return (
      self.cur_selector.match(element_stack, index, match_anywhere=match_anywhere, match_children=match_children) and 
      self.next_selector.match(element_stack, index +1, match_anywhere=match_anywhere, match_children=match_children)
    )

  @classmethod
  def from_stack (cls, selector_stack:list[ISelector]) -> Self:
    next_selector = selector_stack.pop()
    cur_selector = selector_stack.pop()
    return cls(cur_selector, next_selector)

@dataclass
class Selector_MatchAnywhere (ISelector, IGeneratableFromStack):

  """引数 `match_anywhere` が有効ならば、任意の位置からの一致を検証します。

  Notes
  -----
  関数 `parse_selector` によって作成された `ISelector` インスタンスは必ず本オブジェクトを所有します。

  Attributes
  ----------
  selector : ISelector
    一致を試みるセレクターです。
  """

  selector:ISelector

  def match (self, element_stack:list[Element], index:int=0, *, match_anywhere:bool=True, match_children:bool=False) -> bool:
    if match_anywhere:
      return any((self.selector.match(element_stack, i, match_anywhere=match_anywhere, match_children=match_children) for i in range(len(element_stack))))
    else:
      return self.selector.match(element_stack, 0, match_anywhere=match_anywhere, match_children=match_children)


  @classmethod
  def from_stack (cls, selector_stack:list[ISelector]) -> Self:
    selector = selector_stack.pop()
    return cls(selector)

@dataclass
class Selector_MatchLast (ISelector):

  """引数 `match_children` が有効ならば、引数 `element_stack` の終端に一致します。

  Notes
  -----
  関数 `parse_selector` によって作成された `ISelector` インスタンスは必ず本オブジェクトを所有します。
  """

  def match (self, element_stack:list[Element], index:int=0, *, match_anywhere:bool=True, match_children:bool=False) -> bool:
    if match_children:
      return True
    else:
      return index == len(element_stack)

@dataclass
class Selector_Or (ISelector):

  """...

  Attributes
  ----------
  selectors : list[ISelector]
    ...
  """

  selectors:list[ISelector]

  def match (self, element_stack:list[Element], index:int=0, *, match_anywhere:bool=True, match_children:bool=False) -> bool:
    return any((sel.match(element_stack, index, match_anywhere=match_anywhere, match_children=match_children) for sel in self.selectors))

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

SEPARATOR_CHARS:set[str] = set(",> ")

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

def _build (read_selector_stack:list[ISelector], combination_selector_type_stack:list[Type[IGeneratableFromStack]], source_and_pos:tuple[str, int]) -> ISelector:
  if read_selector_stack:
    sel_stack = [] + read_selector_stack + [Selector_MatchLast()]
    comb_sel_type_stack = [Selector_MatchAnywhere] + combination_selector_type_stack + [Selector_Son]
    while comb_sel_type_stack:
      comb_sel_type = comb_sel_type_stack.pop()
      comb_sel = comb_sel_type.from_stack(sel_stack)
      sel_stack.append(comb_sel)
    return sel_stack[-1]
  else:
    raise ParseError.at("Argument `read_selector_stack` given an empty list.", source_and_pos)

def parse_selector (source:str) -> ISelector:

  """CSSセレクターが記述された文字列を受け取り、マッチング用のオブジェクトを作成します。

  Parameters
  ----------
  source : str
    解析するコードが記述された文字列です。

  Returns
  -------
  ISelector
    パースされた `ISelector` インスタンスです。
  """

  read_sel_stack = []
  comb_sel_type_stack = []
  built_sels = []

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
    read_sel_stack.append(sel)
    if index < end:
      separator, index = _read_separator(source, index, end)
      match separator.strip():
        case "":
          comb_sel_type_stack.append(Selector_Children)
        case ">":
          comb_sel_type_stack.append(Selector_Son)
        case ",":
          built_sel = _build(read_sel_stack, comb_sel_type_stack, (source, index))
          built_sels.append(built_sel)
        case _:
          raise ParseError.at("Read unknown separator: {:s}".format(repr(separator)), (source, index))
    else:
      built_sel = _build(read_sel_stack, comb_sel_type_stack, (source, index))
      built_sels.append(built_sel)
      break
  
  if built_sels:
    if len(built_sels) == 1:
      return built_sels[0]
    else:
      return Selector_Or(built_sels)
  else:
    raise ParseError("Could not build ISelector instance even once from source: {:s}".format(repr(source)))
