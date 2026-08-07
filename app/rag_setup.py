import os
import shutil

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


CHROMA_DIR = "chroma_store"


def load_docs(doc_paths):
    """Load TXT and PDF documents."""

    docs = []

    for path in doc_paths:

        ext = os.path.splitext(path)[-1].lower()

        if ext == ".txt":
            loader = TextLoader(
                path,
                encoding="utf-8"
            )

        elif ext == ".pdf":
            loader = PyPDFLoader(path)

        else:
            continue

        loaded_docs = loader.load()

        for doc in loaded_docs:
            doc.metadata["source"] = path

        docs.extend(loaded_docs)

    return docs


def setup_chroma(doc_paths):
    """
    Create a fresh Chroma vector store for the
    currently uploaded documents.
    """

    docs = load_docs(doc_paths)

    if not docs:
        raise ValueError(
            "No supported documents were found."
        )

    # --------------------------------------------------
    # Remove previous Chroma database
    # --------------------------------------------------

    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    # --------------------------------------------------
    # Split documents
    # --------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    # --------------------------------------------------
    # Create embeddings
    # --------------------------------------------------

    embeddings = OpenAIEmbeddings()

    # --------------------------------------------------
    # Create fresh vector database
    # --------------------------------------------------

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    return vectorstore


def retrieve(query, vectorstore, k=5):
    """Retrieve relevant chunks from uploaded documents.
    Uses broader retrieval for list/all/extraction questions."""

    if vectorstore is None:
        return []

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        }
    )

    return retriever.invoke(query)