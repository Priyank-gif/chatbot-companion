# models.py
from pydantic import BaseModel, Field
from typing_extensions import List


class UrlsModel(BaseModel):
    urls: List[str]

class QueryModel(BaseModel):
    query: str

class TextModel(BaseModel):
    text: str = Field(..., example="Enter your text here to be vectorized")
