from pydantic import BaseModel


class Message(BaseModel):
    message: str

class CollectDataResponse(BaseModel):
    status: str
    total_inserted: int
    categories: list 