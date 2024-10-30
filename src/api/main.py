import os

from botocore.exceptions import ClientError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from config import load_aws_client
from models.query_model import QueryModel
from scripts.main import query_rag

app = FastAPI()
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")


class SubmitQueryRequest(BaseModel):
    query_text: str = Field(default="Total revenue in Q1 2024?")


@app.post("/submit_query")
def submit_query_endpoint(request: SubmitQueryRequest) -> QueryModel:
    new_query = QueryModel(query_text=request.query_text)
    query_response = query_rag(request.query_text)
    new_query.answer_text = query_response.response_text
    new_query.sources = query_response.sources
    new_query.is_complete = True
    new_query.put_item()

    return new_query


@app.post("/create_table")
def create_table_endpoint():
    client = load_aws_client("dynamodb")
    try:
        response = client.describe_table(TableName=TABLE_NAME)
        return {
            "message": f"Table '{TABLE_NAME}' already exists.",
            "table_info": response,
        }
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            # Table does not exist, so we create it
            try:
                response = client.create_table(
                    TableName=TABLE_NAME,
                    KeySchema=[
                        {"AttributeName": "query_id", "KeyType": "HASH"},
                    ],
                    AttributeDefinitions=[
                        {"AttributeName": "query_id", "AttributeType": "S"},
                    ],
                    ProvisionedThroughput={
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                )
                return {
                    "message": f"Table '{TABLE_NAME}' created successfully.",
                    "table_info": response,
                }
            except ClientError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to create table: {e.response['Error']['Message']}",
                )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {e.response['Error']['Message']}",
            )
