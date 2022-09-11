from pydantic import BaseModel


class SearchResponseEntry(BaseModel):
    title: str
    extract: str


class SearchResponse(BaseModel):
    results: list[SearchResponseEntry]
