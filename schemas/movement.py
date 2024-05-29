from pydantic import BaseModel


class MovementRequest(BaseModel):
    name: str
    letter: str
    product: str
    before: str
    after: str

