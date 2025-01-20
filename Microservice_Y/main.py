from Endpoint.methods import broker
from faststream import FastStream
import asyncio

app = FastStream(broker)

async def main():
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())