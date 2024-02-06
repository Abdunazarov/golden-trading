# stdlib
import asyncio

# thirdparty
from aio_pika import connect, IncomingMessage


RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def on_message(message: IncomingMessage):
    async with message.process():
        print("Received message", message.body.decode())
        with open("messages.txt", "a") as file:
            file.write(message.body.decode() + "\n")


async def main():
    connection = await connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue("queue", durable=True)

        await queue.consume(on_message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
