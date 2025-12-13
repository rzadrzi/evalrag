# core/config/core_config.py

from dataclasses import dataclass
from pathlib import Path
import os
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = BASE_DIR / "configs" / "core.yaml"


def _load_yaml_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


_yaml_cfg = _load_yaml_config()


def _get(path: str, default=None):
    parts = path.split(".")
    cur = _yaml_cfg
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


@dataclass
class RagConfig:
    top_k: int = _get("rag.top_k", 5)
    max_context_tokens: int = _get("rag.max_context_tokens", 2000)
    model_name: str = _get(
        "rag.model_name", os.getenv("RAG_MODEL_NAME", "gpt-4.1-mini")
    )
    embedding_model: str = _get(
        "rag.embedding_model", os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    )


@dataclass
class EvalConfig:
    judge_model: str = _get(
        "eval.judge_model", os.getenv("JUDGE_MODEL_NAME", "gpt-4.1-mini")
    )
    correctness_weight: float = _get("eval.correctness_weight", 0.5)
    faithfulness_weight: float = _get("eval.faithfulness_weight", 0.3)
    context_relevance_weight: float = _get("eval.context_relevance_weight", 0.2)

    faithfulness_threshold: float = _get("eval.faithfulness_threshold", 3.5)


@dataclass
class IngestionConfig:
    default_chunk_size: int = _get("ingestion.default_chunk_size", 800)
    default_chunk_overlap: int = _get("ingestion.default_chunk_overlap", 100)


@dataclass
class CoreSettings:
    rag: RagConfig = RagConfig()
    eval: EvalConfig = EvalConfig()
    ingestion: IngestionConfig = IngestionConfig()


settings = CoreSettings()
