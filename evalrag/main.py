from core import Ingestion
from core import load_core_config
from pathlib import Path

path  = Path(__file__).resolve().parent / "sample.pdf"

config = load_core_config().ingestion

ingestion = Ingestion(config=config)
ingestion.indexing(filename=str(path))
print(config)
print(path)