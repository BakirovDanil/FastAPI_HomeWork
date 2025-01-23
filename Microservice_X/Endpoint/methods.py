from fastapi import APIRouter
from faststream.rabbit import RabbitBroker
from faststream.rabbit.fastapi import RabbitRouter
import os

tasks = APIRouter()
rabbitmq_url = os.getenv("RABBITMQ_URL")
broker = RabbitBroker(rabbitmq_url)
router = RabbitRouter(rabbitmq_url)

@tasks.get("/setup_database")
async def setup_base():
    result = await broker.publish(queue = "setup_table")
    return result

@tasks.get("/get_all_task",
           tags = ["Получение данных"],
           summary = "Получить данные о всех задачах")
async def get_all_data():
    result = await broker.publish(queue = "get_all_task", rpc = True)
    return result

@tasks.get("/get_id_task",
           tags=["Получение данных"],
           summary="Получить данные о задачи по ID")
async def get_id_data(index: int):
    result = await broker.publish(index, queue = "get_id_task", rpc = True)
    return result

@tasks.post("/create_task",
            tags=["Изменение задач"],
            summary="Добавление задачи")
async def create_task(value: int):
    result = await broker.publish({'value': value}, queue = "create_task", rpc = True)
    return result

@tasks.post("/run_task",
            tags=["Изменение задач"],
            summary="Запуск задачи")
async def run_task(index: int):
    result = await broker.publish(index, queue = "run_task", rpc = False)
    return result

@router.subscriber("get_result")
async def get_result(answer: dict):
    print(answer)