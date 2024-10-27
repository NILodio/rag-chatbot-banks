from dataclasses import dataclass
from typing import List


@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]
