from typing import List, Optional, Union

from pydantic import BaseModel
from schemas.tags import TagsInputSchema, TagsOutputSchema


class NotesOutputSchema(BaseModel):
    id: Union[int, None] = None
    title: str
    description: str
    tags: Union[List[TagsOutputSchema], None] = None


class NotesInputSchema(BaseModel):
    title: str
    description: str
    tags: Union[List[TagsInputSchema], None] = None
