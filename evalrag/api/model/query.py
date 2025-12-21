from pydantic import BaseModel
from typing import Optional, List


class QueryRequestBody(BaseModel):
    query: str
    file_id: str
    k: int = 4
    entity_id: Optional[str] = None


class QueryMultipleBody(BaseModel):
    query: str
    file_ids: List[str]
    k: int = 4
