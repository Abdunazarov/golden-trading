# stdlib
from typing import Optional
from datetime import datetime

# thirdparty
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

# project 
from services.rabbitmq_send_service import send_message


rabbitmq_router = APIRouter(prefix="/rabbitmq", tags=["RABBITMQ"])


@rabbitmq_router.post("/send/{queue_name}")
async def send(queue_name: str, message: str):
    try:
        await send_message(queue_name, message)
        return {"message": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

