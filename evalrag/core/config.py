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
VECTOR_STORE = BASE_DIR / "evalrag" / "core"


def _load_yaml_config() -> dict:
    """
    Load the core YAML configuration file.

    Returns a dictionary parsed from `CONFIG_FILE` (configs/core.yaml) if
    it exists, otherwise returns an empty dict.
    """

    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


_yaml_cfg = _load_yaml_config()


def _get(path: str, default=None) -> Any:
    """
    Retrieve a value from the loaded YAML config using a dotted path.

    Example: `_get("rag.top_k")` will look for `{"rag": {"top_k": ...}}`
    in the parsed YAML and return the value if present, otherwise return
    the provided `default`.
    """

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
    top_k: int = _get("rag.top_k", 5)
    max_context_tokens: int = _get("rag.max_context_tokens", 2000)
    provider: str = _get("rag.provider", os.getenv("PROVIDER", "HF"))
    vector_store_path: str = str(VECTOR_STORE)



@dataclass
class EvalConfig:
    """
    Configuration for evaluation metrics and judge settings.

    Holds weighting values and thresholds used by the evaluation subsystem.
    """
    judge_provider: str = _get("eval.judge_provider", os.getenv("JUDGE_PROVIDER", "HF"))
    correctness_weight: float = _get("eval.correctness_weight", 0.5)
    faithfulness_weight: float = _get("eval.faithfulness_weight", 0.3)
    context_relevance_weight: float = _get("eval.context_relevance_weight", 0.2)

    faithfulness_threshold: float = _get("eval.faithfulness_threshold", 3.5)



@dataclass
class IngestionConfig:
    """
    Configuration for document ingestion and chunking.

    Fields include default chunk sizing and the data/vector store paths.
    """
    default_chunk_size: int = _get("ingestion.default_chunk_size", 800)
    default_chunk_overlap: int = _get("ingestion.default_chunk_overlap", 100)
    provider: str = _get("rag.provider", os.getenv("PROVIDER", "HF"))
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


def _load_prompt_config() -> dict:
    """
    Load the prompt YAML file and return the parsed structure.

    Returns an empty dict when the prompt file is not present.
    """

    if PROMPTS_FILE.exists():
        print("Loading prompt config from:", PROMPTS_FILE)
        with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

_prompt_cfg = _load_prompt_config()


@dataclass
class PromptConfig:
    """
    Configuration for prompt templates.

    Fields:
        - `prompt_template`: The template string used for RAG prompts.
        - `judge_template`: The template string used for judge evaluations.
    """
    prompt_template: str = _prompt_cfg.get(
        "prompt_template", 
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
    
    judge_template: str = _prompt_cfg.get(
        "judge_template",
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
