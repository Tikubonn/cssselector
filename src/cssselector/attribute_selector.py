
import html
from abc import ABC, abstractmethod
from dataclasses import dataclass
from .exception import ParseError

class IAttributeSelector (ABC):

  """属性セレクターを表現するインターフェイスです。"""

  @abstractmethod
  def match (self, attrs:dict[str, str]) -> bool:

    """要素に設定された属性が自身の条件に一致するかを判定します。

    Parameters
    ----------
    attrs : dict[str, str]
      要素に設定された属性の集合です。

    Returns
    -------
    bool
      属性が自身の条件に一致するならば `True` そうでなければ `False` を返します。
    """

    pass

@dataclass
class AttributeSelector_HasName (IAttributeSelector):

  """指定属性名が存在していればマッチする属性セレクターです。

  Parameters
  ----------
  name : str
    指定する属性名です。
  """

  name:str

  def match (self, attrs:dict[str, str]) -> bool:
    return self.name in attrs

@dataclass
class AttributeSelector_Equal (IAttributeSelector):

  """指定属性名が指定値と一致するならばマッチする属性セレクターです。

  Parameters
  ----------
  name : str
    指定する属性名です。
  value : str
    指定する属性値です。
  """

  name:str
  value:str

  def match (self, attrs:dict[str, str]) -> bool:
    return self.name in attrs and attrs[self.name] == self.value

@dataclass
class AttributeSelector_StartsWith (IAttributeSelector):

  """指定属性名が指定値と一致するならばマッチする属性セレクターです。

  Parameters
  ----------
  name : str
    指定する属性名です。
  value : str
    指定する属性値です。
  """

  name:str
  value:str

  def match (self, attrs:dict[str, str]) -> bool:
    return self.name in attrs and attrs[self.name].startswith(self.value)

@dataclass
class AttributeSelector_EndsWith (IAttributeSelector):

  """指定属性値の先頭が指定値で始まるならばマッチする属性セレクターです。

  Parameters
  ----------
  name : str
    指定する属性名です。
  value : str
    指定する属性値です。
  """

  name:str
  value:str

  def match (self, attrs:dict[str, str]) -> bool:
    return self.name in attrs and attrs[self.name].endswith(self.value)

@dataclass
class AttributeSelector_ContainsAnywhere (IAttributeSelector):

  """指定属性値の末尾が指定値で終わるならばマッチする属性セレクターです。

  Parameters
  ----------
  name : str
    指定する属性名です。
  value : str
    指定する属性値です。
  """

  name:str
  value:str

  def match (self, attrs:dict[str, str]) -> bool:
    return self.name in attrs and self.value in attrs[self.name]

@dataclass
class AttributeSelector_ContainsWithSeparator (IAttributeSelector):

  """指定値が空白文字で区切られた指定属性値のリストに存在していればマッチする属性セレクターです。

  Examples
  --------
  >>> sel = AttributeSelector_ContainsWithSeparator("a", "b")
  >>> sel.match({"a": "a b c"})
  True

  Parameters
  ----------
  name : str
    指定する属性名です。
  value : str
    指定する属性値です。
  """

  name:str
  value:str

  def match (self, attrs:dict[str, str]) -> bool:
    return self.name in attrs and self.value in attrs[self.name].split(" ")

#parser

ATTRIBUTE_NAME_START_CHARS:set[str] = set(":ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz")
ATTRIBUTE_NAME_CHARS:set[str] = set("-.0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz")

def _read_attribute_name (source:str, start:int, end:int) -> tuple[str, int]:
  if start < end:
    if source[start] in ATTRIBUTE_NAME_START_CHARS:
      tmp = source[start]
      index = start +1
      while index < end and source[index] in ATTRIBUTE_NAME_CHARS:
        tmp += source[index]
        index += 1
      return tmp, index
    else:
      raise ParseError.at("Read an invalid character to start of attribute name: {:s}".format(repr(source[start])), (source, start))
  else:
    raise ParseError.at("Reached end of data on parsing.", (source, start))

def _read_attribute_value (source:str, start:int, end:int) -> tuple[str, int]:
  if start < end:
    if source[start] == "\"":
      tmp = ""
      index = start +1
      while index < end and source[index] != "\"":
        tmp += source[index]
        index += 1
      if index < end:
        if source[index] == "\"":
          index += 1
        else:
          raise ParseError.at("Could not read '\"' to end of attribute value: {:s}".format(repr(source[start])), (source, start))
      else:
        raise ParseError.at("Reached end of data on parsing.", (source, start))
      if index < end:
        if source[index] == "]":
          index += 1
        else:
          raise ParseError.at("Could not read '[' after '\"' to end of attribute value: {:s}".format(repr(source[start])), (source, start))
      else:
        raise ParseError.at("Reached end of data on parsing.", (source, start))
      return html.unescape(tmp), index
    else:
      raise ParseError.at("Could not read '\"' to start of attribute value: {:s}".format(repr(source[start])), (source, start))
  else:
    raise ParseError.at("Reached end of data on parsing.", (source, start))

def parse_attribute_selector (source:str, start:int, end:int) -> tuple[IAttributeSelector, int]:

  """属性セレクターのコードをパースします。

  Parameters
  ----------
  source : str
    パースするコードが記述された文字列です。
  start : int
    有効なコードの開始位置です。
    この引数は `source` の先頭に空白文字が存在しなければ `0` を指定するのが望ましいです。
  end : int
    有効なコードの終了位置です。
    この引数は `source` の先頭に空白文字が存在しなければ `source` の総文字数を指定するのが望ましいです。

  Returns
  -------
  tuple[IAttributeSelector, int]
    パースされた `IAttributeSelector` インスタンスです。
  """

  if start < end:
    if source[start] == "[":
      index = start +1
      name, index = _read_attribute_name(source, index, end)
      if source[index:].startswith("]"):
        return AttributeSelector_HasName(name), index +1
      elif source[index:].startswith("^="):
        value, index = _read_attribute_value(source, index +2, end)
        return AttributeSelector_StartsWith(name, value), index
      elif source[index:].startswith("$="):
        value, index = _read_attribute_value(source, index +2, end)
        return AttributeSelector_EndsWith(name, value), index
      elif source[index:].startswith("*="):
        value, index = _read_attribute_value(source, index +2, end)
        return AttributeSelector_ContainsAnywhere(name, value), index
      elif source[index:].startswith("~="):
        value, index = _read_attribute_value(source, index +2, end)
        return AttributeSelector_ContainsWithSeparator(name, value), index
      elif source[index:].startswith("="):
        value, index = _read_attribute_value(source, index +1, end)
        return AttributeSelector_Equal(name, value), index
      else:
        raise ParseError.at("Could not read any supported operator.", (source, start))
    else:
      raise ParseError.at("Could not read '[' to start of attribute selector: {:s}".format(repr(source[start])), (source, start))
  else:
    raise ParseError.at("Reached end of data on parsing.", (source, start))
