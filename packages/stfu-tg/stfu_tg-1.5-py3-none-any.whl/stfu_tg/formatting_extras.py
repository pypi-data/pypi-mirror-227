from typing import Any

from .formatting import Bold
from .formatting import Core


class Title(Core):
    def __init__(self, item: Any, prefix='[', postfix=']', bold: bool = True):
        self.item = str(item)
        self.prefix = prefix
        self.postfix = postfix
        self.bold = bold

    def __str__(self) -> str:
        text = f"{self.prefix}{self.item}{self.postfix}"

        if self.bold:
            text = str(Bold(text))

        return text
