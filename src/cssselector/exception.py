
from typing import Self

class ParseError (Exception):

  @classmethod
  def at (cls, message:str, source_and_pos:tuple[str, int]) -> Self:
    source, pos = source_and_pos
    return cls("{:s} ({:s} at {:d})".format(message, repr(source), pos))
