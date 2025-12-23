# evalrag/core/config.py

from dataclasses import dataclass
from pathlib import Path
import os
from typing import Any
import yaml

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_FILE = BASE_DIR / "configs" / "core.yaml"
PROMPTS_FILE = BASE_DIR / "configs" / "prompt.yaml"
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE = BASE_DIR / "evalrag" / "vectorDB"


def _load_yaml_config(filename) -> dict:
    """
    Load the core YAML configuration file.

    Returns a dictionary parsed from `filename`
    
    if it exists, otherwise returns an empty dict.
    """

    if filename.exists():
        with open(filename, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def _get(filename, path: str, default=None) -> Any:
    """
    Retrieve a value from the loaded YAML config using a dotted path.

    Example: `_get("rag.top_k")` will look for `{"rag": {"top_k": ...}}`
    in the parsed YAML and return the value if present, otherwise return
    the provided `default`.
    """
    _yaml_cfg = _load_yaml_config(filename)


    parts = path.split(".")
    cur = _yaml_cfg
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


@dataclass
class RagConfig:
    """
    Configuration for RAG (retrieval-augmented generation).

    Fields:
        - `top_k`: default number of retrieved contexts.
        - `max_context_tokens`: max tokens allowed from contexts.
        - `provider`: embeddings/LLM provider (e.g. "HF" or "OPENAI").
        - `vector_store_path`: filesystem path where the vector store resides.
    """
    top_k: int = _get(CONFIG_FILE, "rag.top_k", 5)
    max_context_tokens: int = _get(CONFIG_FILE, "rag.max_context_tokens", 2000)
    provider: str = _get(CONFIG_FILE, "rag.provider", os.getenv("PROVIDER", "HF"))
    vector_store_path: str = str(VECTOR_STORE)


@dataclass
class EvalConfig:
    """
    Configuration for evaluation metrics and judge settings.

    Holds weighting values and thresholds used by the evaluation subsystem.
    """
    judge_provider: str = _get(CONFIG_FILE, "eval.judge_provider", os.getenv("JUDGE_PROVIDER", "HF"))
    correctness_weight: float = _get(CONFIG_FILE, "eval.correctness_weight", 0.5)
    faithfulness_weight: float = _get(CONFIG_FILE, "eval.faithfulness_weight", 0.3)
    context_relevance_weight: float = _get(CONFIG_FILE, "eval.context_relevance_weight", 0.2)

    faithfulness_threshold: float = _get(CONFIG_FILE, "eval.faithfulness_threshold", 3.5)


@dataclass
class IngestionConfig:
    """
    Configuration for document ingestion and chunking.

    Fields include default chunk sizing and the data/vector store paths.
    """
    default_chunk_size: int = _get(CONFIG_FILE, "ingestion.default_chunk_size", 800)
    default_chunk_overlap: int = _get(CONFIG_FILE, "ingestion.default_chunk_overlap", 100)
    provider: str = _get(CONFIG_FILE, "rag.provider", os.getenv("PROVIDER", "HF"))
    data_dir: str = str(DATA_DIR)
    vector_store_path: str = str(VECTOR_STORE)


@dataclass
class CoreSettings:
    """
    Aggregated core settings dataclass combining `RagConfig`,
    `EvalConfig`, and `IngestionConfig`.
    """
    rag: RagConfig
    eval: EvalConfig
    ingestion: IngestionConfig


def load_core_config() -> CoreSettings:
    """
    Build and return the aggregated `CoreSettings` object.

    This creates instances of the individual dataclass configs and returns
    a single `CoreSettings` instance for easy access by the application.
    """

    config = CoreSettings(
        rag=RagConfig(), eval=EvalConfig(), ingestion=IngestionConfig()
    )
    return config



@dataclass
class PromptConfig:
    """
    Configuration for prompt templates.

    Fields:
        - `prompt_template`: The template string used for RAG prompts.
        - `judge_template`: The template string used for judge evaluations.
    """
    prompt_template: str = _get(PROMPTS_FILE, "prompt.template",
        """You are an assistant that answers questions based only on the provided context.

        Question:
        {question}

        Context:
        {context_block}

        Instructions:
        - If the answer is not in the context, say you don't know.
        - Answer in a concise and precise way.

        Answer:
        """)
    
    judge_template: str = _get(PROMPTS_FILE, "prompt.judge",
        """You are a judge that evaluates the quality of answers based on provided contexts.

        Question:
        {question}

        Answer:
        {answer}

        Context:
        {context_block}

        Evaluation Criteria:
        - Correctness: Is the answer factually correct?
        - Faithfulness: Does the answer accurately reflect the context?
        - Relevance: Is the context relevant to the question?

        Provide a score from 1 to 5 for each criterion and a brief explanation.
        """)


def load_prompt_config() -> PromptConfig:
    """
    Retrieve the `PromptConfig` instance with loaded templates.

    Returns an instance of `PromptConfig` containing the prompt and
    judge templates.
    """

    return PromptConfig()
