import os
import shutil

import typer
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock

from config import PROMPT_TEMPLATE, load_aws_client
from models.chroma_database import ChromaDatabase
from models.rag import QueryResponse
from utils.document_loader import generate_chunk_ids, load_documents, split_documents

load_dotenv()

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def populate_database(
    chroma_path: str,
    source_path: str,
    model_id: str = "amazon.titan-embed-text-v1",
    clear: bool = False,
):
    if clear:
        if os.path.exists(chroma_path):
            shutil.rmtree(chroma_path)
    aws_client = load_aws_client("bedrock-runtime")
    chroma_db = ChromaDatabase(
        chroma_path=chroma_path, model_id=model_id, bedrock_client=aws_client
    )

    documents = load_documents(source_path=source_path)
    chunks = split_documents(
        documents,
        chunk_size=600,
        chunk_overlap=120,
        length_function=len,
        is_separator_regex=False,
    )
    chunks_with_ids = generate_chunk_ids(chunks)
    existing_ids = chroma_db.get_existing_ids()
    new_chunks = [
        chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids
    ]
    if new_chunks:
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        chroma_db.add_documents(new_chunks, new_chunk_ids)


@app.command()
def query_rag(
    query_text: str,
    chroma_path: str = "data/chroma",
    model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
) -> QueryResponse:
    aws_client = load_aws_client("bedrock-runtime")
    chroma_db = ChromaDatabase(chroma_path=chroma_path, bedrock_client=aws_client)
    db = chroma_db.get_chroma_db()
    results = db.similarity_search_with_score(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    model = ChatBedrock(client=aws_client, model_id=model_id)
    response = model.invoke(prompt)
    response_text = response.content

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {response_text}\nSources: {sources}")
    return QueryResponse(
        query_text=query_text, response_text=response_text, sources=sources
    )


if __name__ == "__main__":
    app()
