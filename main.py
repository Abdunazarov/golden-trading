# thirdparty
from fastapi import FastAPI

# project
from routers.authentication import authentication_router
from routers.users import users_router

app = FastAPI()

app.include_router(authentication_router)
app.include_router(users_router)
