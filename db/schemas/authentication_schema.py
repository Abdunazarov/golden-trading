# stdlib
import datetime
from typing import List, Optional

# thirdparty
from pydantic import BaseModel, Field, EmailStr

class UserCreateBody(BaseModel):
    username: str = Field(..., min_length=6, max_length=36)
    email: EmailStr
    password: str
    fio: str = Field(..., max_length=200)
    birthday: Optional[datetime.date]
    tags: List[str]


class RegisterResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    fio: str
    birthday: Optional[datetime.date]
    tags: List[str]
