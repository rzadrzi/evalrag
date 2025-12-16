# _indexing.py
from config import config

from ingestion import pdf_loader

path = config.ingestion.data_dir

pdf_loader(path)
