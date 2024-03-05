import pydantic

from fastapi import FastAPI
from search import search, NodeWithScore
from fastapi.middleware.cors import CORSMiddleware


class SearchRequest(pydantic.BaseModel):
    url: str | None = None
    html: str | None = None
    query: str

    @pydantic.root_validator(pre=True)
    def validate_source(cls, values):
        if sum(bool(v) for v in (values.get("url", 0), values.get("html", 0))) != 1:
            raise ValueError("Either url or html must be set.")

        return values


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
    print(req)
    retrieved_documents: list[NodeWithScore] = search(req.url, req.html, req.query)
    return [
        SearchResponse(text=document.get_text(), score=document.score)
        for document in retrieved_documents
    ]
