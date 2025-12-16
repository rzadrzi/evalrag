# __init__.py

from .config import load_config
from .ingestion import pdf_loader

config = load_config()

__all__ = ["config", "pdf_loader"]
