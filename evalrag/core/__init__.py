# __init__.py

from .config import load_config

config = load_config()
__all__ = ["config"]
