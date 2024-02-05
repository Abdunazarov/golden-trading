# stdlib
import datetime
from typing import List

# thirdparty
from pydantic import BaseModel, Field, EmailStr


class SingleUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    config: str


class UsersResponse(BaseModel):
    results: List[SingleUserResponse]
