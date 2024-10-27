from fastapi import FastAPI
from pydantic import BaseModel

from models.query_model import QueryModel
from scripts.main import query_rag

app = FastAPI()


class SubmitQueryRequest(BaseModel):
    query_text: str


@app.post("/submit_query")
def submit_query_endpoint(request: SubmitQueryRequest) -> QueryModel:
    new_query = QueryModel(query_text=request.query_text)
    query_response = query_rag(request.query_text)
    new_query.answer_text = query_response.response_text
    new_query.sources = query_response.sources
    new_query.is_complete = True
    new_query.put_item()

    return new_query
