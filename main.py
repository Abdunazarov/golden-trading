# stdlib
import time
from datetime import datetime

# thirdparty
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

# project
from routers.authentication import authentication_router
from routers.users import users_router

app = FastAPI()

# routers
app.include_router(authentication_router)
app.include_router(users_router)


# middleware for logging
class Logging(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        body = await request.body()
        request_time = datetime.utcnow()
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        print(
            f"""
            Request info:
            Method: {request.method}
            URL: {request.url}
            Body: {body}
            Time: {request_time}
            Process time: {process_time:.2f}
            Response status: {response.status_code}
        """
        )

        return response


app.add_middleware(Logging)
