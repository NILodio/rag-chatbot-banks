import os
import time
import uuid
from typing import List, Optional

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from config import load_aws_client

load_dotenv()

TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")  # Ensure you have this in your .env


class QueryModel(BaseModel):
    query_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    create_time: int = Field(default_factory=lambda: int(time.time()))
    query_text: str
    answer_text: Optional[str] = None
    sources: List[str] = Field(default_factory=list)
    is_complete: bool = False

    @classmethod
    def get_client(cls: "QueryModel") -> boto3.client:
        return load_aws_client("dynamodb")

    @classmethod
    def describe_table(cls: "QueryModel"):
        client = cls.get_client()
        try:
            response = client.describe_table(TableName=TABLE_NAME)
        except ClientError as e:
            print("ClientError", e.response["Error"]["Message"])
            raise e
        return response

    @classmethod
    def create_table(cls: "QueryModel"):
        client = cls.get_client()
        try:
            response = client.create_table(
                TableName=TABLE_NAME,
                KeySchema=[
                    {"AttributeName": "query_id", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "query_id", "AttributeType": "S"},
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            print("Table creation initiated:", response)
        except ClientError as e:
            print("ClientError", e.response["Error"]["Message"])
            raise e

    def put_item(self):
        item = self.as_ddb_item()
        print(item)
        print(TABLE_NAME)
        try:
            response = QueryModel.get_client().put_item(TableName=TABLE_NAME, Item=item)
            print(response)
        except ClientError as e:
            print("ClientError", e.response["Error"]["Message"])
            raise e

    def as_ddb_item(self):
        item = {k: {"S": str(v)} for k, v in self.dict().items() if v is not None}
        return item

    @classmethod
    def get_item(cls: "QueryModel", query_id: str) -> "QueryModel":
        try:
            response = cls.get_client().get_item(
                TableName=TABLE_NAME, Key={"query_id": {"S": query_id}}
            )
        except ClientError as e:
            print("ClientError", e.response["Error"]["Message"])
            return None

        if "Item" in response:
            item = response["Item"]
            return cls(**{k: v["S"] for k, v in item.items()})
        else:
            return None
