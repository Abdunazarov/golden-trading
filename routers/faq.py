# thirdparty
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from elasticsearch import Elasticsearch, NotFoundError

faq_router = APIRouter(prefix="/faq", tags=["FAQ"])
es = Elasticsearch(
    "http://localhost:9200", basic_auth=("elastic", "zWrI2xttWcEy7Vx=+39a")
)


class FAQ(BaseModel):
    question: str
    answer: str


@faq_router.post("")
async def create_faq(faq: FAQ):
    res = es.index(index="faq", document=faq.model_dump())
    return {"result": "Created", "id": res["_id"]}


@faq_router.get("/{faq_id}")
async def get_faq(faq_id: str):
    try:
        res = es.get(index="faq", id=faq_id)
        return res["_source"]
    except NotFoundError:
        raise HTTPException(status_code=404, detail="FAQ not found")


@faq_router.get("/search/")
async def search_faq(query: str):
    res = es.search(index="faq", query={"match": {"question": query}})
    return [doc["_source"] for doc in res["hits"]["hits"]]


@faq_router.put("/{faq_id}")
async def update_faq(faq_id: str, faq: FAQ):
    try:
        es.update(index="faq", id=faq_id, doc=faq.model_dump())
        return {"result": "Updated"}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="FAQ not found")


@faq_router.delete("/{faq_id}")
async def delete_faq(faq_id: str):
    try:
        es.delete(index="faq", id=faq_id)
        return {"result": "Deleted"}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="FAQ not found")
