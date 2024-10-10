from typing import Callable

from langchain.schema.document import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(source_path: str):
    document_loader = PyPDFDirectoryLoader(source_path)
    return document_loader.load()


def split_documents(
    documents: list[Document],
    chunk_size: int,
    chunk_overlap: int,
    length_function: Callable[[str], int],
    is_separator_regex: bool,
):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function,
        is_separator_regex=is_separator_regex,
    )
    return text_splitter.split_documents(documents)


def generate_chunk_ids(chunks: list[Document]):
    last_page_id = None
    current_chunk_index = 0
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        chunk.metadata["id"] = chunk_id
    return chunks
