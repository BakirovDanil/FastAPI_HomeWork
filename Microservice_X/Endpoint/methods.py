from fastapi import APIRouter
from faststream.rabbit import RabbitBroker
from faststream.rabbit.fastapi import RabbitRouter
import os

tasks = APIRouter()
rabbitmq_url = os.getenv("RABBITMQ_URL")
broker = RabbitBroker(rabbitmq_url)
router = RabbitRouter(rabbitmq_url)

@tasks.get("/setud_database")
async def setup_base():
    result = await broker.publish(queue = "setup_table")
    return result

@tasks.get("/get_all_task")
async def get_all_data():
    result = await broker.publish(queue = "get_all_task", rpc = True)
    return result

@tasks.get("/get_id_task")
async def get_id_data(index: int):
    result = await broker.publish(index, queue = "get_id_task", rpc = True)
    return result

@tasks.post("/create_task")
async def create_task(value: int):
    result = await broker.publish(value, queue = "create_task", rpc = True)
    return result

@tasks.post("/run_task")
async def run_task(index: int):
    result = await broker.publish(index, queue = "run_task", rpc = False)
    return result

@router.subscriber("get_result")
async def get_result(answer: dict):
    print(answer)