from pydantic import BaseModel


class Message(BaseModel):
    message: str

class Categories(BaseModel):
    categories: dict