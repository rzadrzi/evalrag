# indexing.py
from typing import List

from langchain_core.documents import Document
from ingestion.loader import pdf_loader, load_all_pdf
from ingestion.chunkers import text_splitter
from ingestion.embedding import get_embedding_model
from ingestion.vector_store import vector_store_
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import load_config


class Indexing:
    def __init__(self) -> None:
        self.config = load_config().ingestion

        def loader(self) -> List[List[Document]]:
            return load_all_pdf(path=self.config.data_dir)

        def splitter(self):
            docs = []

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.config.default_chunk_size,
                chunk_overlap=self.config.default_chunk_overlap,
                add_start_index=True,
            )

            for doc in self.loader():
                docs.append(text_splitter.split_documents(doc))

            return docs

        """
        splitsits = text_splitter(
            docs=docs,
            chunk_size=setting.default_chunk_size,
            chunk_overlap=setting.default_chunk_overlap,
        )

        embedding = get_embedding_model(provider_name=setting.provider_name)

        vector_store_(
            embeddings=embedding,
            splits=splits,
            vector_store_path=setting.vector_store_path,
        )
        """
