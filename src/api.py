import pydantic

from fastapi import FastAPI
from search import search, NodeWithScore
from fastapi.middleware.cors import CORSMiddleware


class SearchRequest(pydantic.BaseModel):
    url: str
    query: str


class SearchResponse(pydantic.BaseModel):
    text: str
    score: float


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/search/")
async def ai_search(req: SearchRequest) -> list[SearchResponse]:
    retrieved_documents: list[NodeWithScore] = search(req.url, req.query)
    return [
        SearchResponse(text=document.get_text(), score=document.score)
        for document in retrieved_documents
    ]
