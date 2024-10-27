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


class QueryModel(BaseModel):
    query_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    create_time: int = Field(default_factory=lambda: int(time.time()))
    query_text: str
    answer_text: Optional[str] = None
    sources: List[str] = Field(default_factory=list)
    is_complete: bool = False

    @classmethod
    def get_table(cls: "QueryModel") -> boto3.resource:
        dynamodb = load_aws_client("dynamodb")
        return dynamodb.Table(os.getenv("DYNAMODB_TABLE_NAME"))

    def put_item(self):
        item = self.as_ddb_item()
        try:
            response = QueryModel.get_table().put_item(Item=item)
            print(response)
        except ClientError as e:
            print("ClientError", e.response["Error"]["Message"])
            raise e

    def as_ddb_item(self):
        item = {k: v for k, v in self.dict().items() if v is not None}
        return item

    @classmethod
    def get_item(cls: "QueryModel", query_id: str) -> "QueryModel":
        try:
            response = cls.get_table().get_item(Key={"query_id": query_id})
        except ClientError as e:
            print("ClientError", e.response["Error"]["Message"])
            return None

        if "Item" in response:
            item = response["Item"]
            return cls(**item)
        else:
            return None
