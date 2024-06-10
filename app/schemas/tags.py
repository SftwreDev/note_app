from pydantic import BaseModel


class TagsInputSchema(BaseModel):
    name: str


class TagsOutputSchema(BaseModel):
    id: int
    name: str
