# evalrag/core/ingestion.py
import os

from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS


class Ingestion:

    """
    Ingestion pipeline helper for building a vector index from files.

    Responsibilities:
      - Discover and load supported files from a directory (currently PDFs).
      - Split documents into chunks suitable for embedding.
      - Provide an embeddings-model factory for supported providers.
      - Build and persist a FAISS-based vector store.

    Typical usage:
      1. `loader(path)` to load source documents.
      2. `splitter(...)` to chunk them for embedding.
      3. `get_embedding_model(provider)` to obtain embeddings.
      4. `vector_store(embeddings, splits, path)` to create and save the index.

    Args:
        config: Configuration object or mapping used by ingestion routines.
    """

    def __init__(self, config) -> None:

        """
        Initialize the Ingestion helper.

        Args:
            config: Configuration object or mapping used by ingestion processes.

        The provided `config` is stored on the instance for later use by
        other methods in this class.
        """
        self.config = config

    def loader(self, filename: str)->List[Document]:
        """
        Load documents from the given filesystem `path`.

        Currently this scans the directory at `path` and loads files it
        recognizes (PDFs) into LangChain `Document` objects using
        `PyPDFLoader`.

        Args:
            filename: Directory path containing files to load.

        Returns:
            A list where each element is a list of `Document` objects
            corresponding to a single source file.
        """

        pdf_loader = PyPDFLoader(filename)
        docs = pdf_loader.load()
        
        return docs

    def splitter(
            self, 
            docs: List[Document], 
            chunk_size: int = 100, 
            chunk_overlap: int = 10
            )->List[Document]:

        """
        Split loaded documents into smaller chunks for embedding/indexing.

        This method accepts a list of document-lists (one inner list per
        source file) and applies `RecursiveCharacterTextSplitter` to each
        to produce chunked `Document` objects suitable for embedding.

        Args:
            docs: List of document lists to split.
            chunk_size: Maximum characters per chunk.
            chunk_overlap: Overlap between adjacent chunks.

        Returns:
            A list where each element is the list of chunked `Document`
            objects derived from the corresponding input document list.
        """

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap, 
            add_start_index=True
            )
        
        return text_splitter.split_documents(docs)
        
    def get_embedding_model(self, provider: str = "HF"):
        """
        Return an embeddings model instance for the requested provider.

        Supported providers:
          - "HF": returns a `HuggingFaceEmbeddings` instance using a
            sentence-transformers model.
          - "OPENAI": returns an `OpenAIEmbeddings` instance.

        Args:
            provider: String identifier for the provider, defaults to "HF".

        Returns:
            An embeddings model object suitable for `embed_query`/`embed_documents`.
        """

        if provider == "HF":
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

        elif provider == "OPENAI":
            return OpenAIEmbeddings(model="text-embedding-3-large")

    def vector_store(
            self, 
            embeddings, 
            splits: List[Document], 
            vector_store_path: str):
        """
        Build a FAISS vector store from provided document splits and save it.

        This creates an in-memory FAISS index using the dimensionality
        inferred from the provided `embeddings` object, wraps it with the
        LangChain `FAISS` helper, adds the given `splits`, and persists the
        index to `vector_store_path`.

        Args:
            embeddings: Embedding model instance with an `embed_query` method.
            splits: List of chunked `Document` objects to add to the store.
            vector_store_path: Filesystem path where the FAISS index will be saved.
        """

        embedding_dim = len(embeddings.embed_query("hello world"))
        index = faiss.IndexFlatL2(embedding_dim)
        store = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
            )
        store.add_documents(splits)
        # store.save_local("../faiss_indexing")
        store.save_local(vector_store_path)

    def indexing(self, filename: str):
        """
        High-level entry point for running the full ingestion + indexing
        pipeline.

        This is a placeholder method intended to orchestrate `loader`,
        `splitter`, `get_embedding_model`, and `vector_store` calls.
        Implementations should call those helpers in sequence to create
        and persist a vector index.
        """
        docs = self.loader(filename=filename)
        
        all_splits = self.splitter(
            docs=docs,
            chunk_size=self.config.default_chunk_size,
            chunk_overlap=self.config.default_chunk_overlap
            )
        
        embeddings = self.get_embedding_model(provider=self.config.provider)
        
        self.vector_store(
            embeddings=embeddings, 
            splits=all_splits, 
            vector_store_path=self.config.vector_store_path
            )


if __name__ == "__main__":
    from pathlib import Path

    from .config import load_core_config
    config = load_core_config().ingestion
    print(config)
    ingestion = Ingestion(config=config)
    # path = Path
    # ingestion.indexing(filename="./sample.pdf")




    # path = "./"
    
    # all_docs = []

    # all_files = os.listdir(path)
    
    # for filename in all_files:
    #     ext = filename.split(".")[-1].lower()
    #     if ext == "pdf":
    #         all_docs.append(filename)