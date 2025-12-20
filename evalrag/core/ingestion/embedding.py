from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


def get_embedding_model(provider_name: str = "HF"):
    embeddings = None
    if provider_name == "HF":
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
    elif provider_name == "OPENAI":
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return embeddings
