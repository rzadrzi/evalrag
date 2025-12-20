# _indexing.py

from config import load_config
from ingestion import pdf_loader, text_splitter, get_embedding_model, vector_store_


def indexing():
    setting = load_config().ingestion

    docs = pdf_loader(path=setting.data_dir)
    chuncks = text_splitter(
        docs=docs,
        chunk_size=setting.default_chunk_size,
        chunk_overlap=setting.default_chunk_overlap,
    )
    embedding_model = get_embedding_model(provider_name=setting.provider_name)

    vector_store_(
        embeddings=embedding_model,
        splits=chuncks,
        vector_store_path=setting.vector_store_path,
    )


if __name__ == "__main__":
    indexing()
