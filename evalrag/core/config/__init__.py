# __init__.py

import sys

print(sys.path)
from .core_config import load_config

__all__ = ["load_config"]
