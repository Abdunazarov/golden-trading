# thirdparty
from fastapi import APIRouter
from fastapi.responses import JSONResponse


authentication_router = APIRouter(prefix="/auth", tags=["AUTHENTICATION"])

@authentication_router.get("/welcome")
async def welcome():
    return JSONResponse("Welcome!")