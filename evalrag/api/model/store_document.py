from pydantic import BaseModel


class StoreDocument(BaseModel):
    filepath: str
    filename: str
    file_content_type: str
    file_id: str
