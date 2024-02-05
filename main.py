# thirdparty
from fastapi import FastAPI

# project
from routers.authentication import authentication_router

app = FastAPI()

app.include_router(authentication_router)


