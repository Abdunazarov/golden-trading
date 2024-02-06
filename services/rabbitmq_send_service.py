
# thirdparty
from aio_pika import connect, Message


# project 
from settings import RABBITMQ_URI

async def send_message(queue_name: str, message: str) -> None:
    connection = await connect(RABBITMQ_URI)
    channel = await connection.channel()

    await channel.declare_queue(queue_name, durable=True)
    await channel.default_exchange.publish(
        Message(message.encode()), routing_key=queue_name
    )

