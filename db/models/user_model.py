# thirdparty
from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy import BigInteger, Column, String, Text, JSON

# project
from db.db_setup import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True, unique=True)
    email = Column(String, nullable=True)
    hashed_password = Column(Text, nullable=False)
    config = Column(JSON, nullable=False)


    def verify_password(self, password):
        try:
            return bcrypt.verify(password, str(self.hashed_password))
        except Exception:
            raise HTTPException(409, "Something went wrong with password")
