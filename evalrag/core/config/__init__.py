# __init__.py

from .core_config import load_config

config = load_config()

__all__ = ["config"]
