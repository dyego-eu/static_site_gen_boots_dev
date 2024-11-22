from enum import Enum, auto
from typing import Optional

from dataclasses import dataclass

class TextNodeTypes(Enum):
    NORMAL = auto()
    BOLD = auto()
    ITALIC  = auto()
    CODE = auto()
    LINK = auto()
    IMG = auto()
    
@dataclass
class TextNode:
    content: str
    node_type: TextNodeTypes
    url: Optional[str] = None

