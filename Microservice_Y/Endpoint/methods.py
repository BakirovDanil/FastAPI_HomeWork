import asyncio
from base.db import  SessionDep, engine, Base
from base.modelORM import TaskORM
from faststream.rabbit import RabbitBroker
from Models.model import TaskSchema
from sqlalchemy import select
import logging

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
logging.basicConfig(
    level = logging.DEBUG,
    filename= "log.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

@broker.subscriber("setup_table")
async def setup_database():
    """
    Настраивает базу данных, удаляя все существующие таблицы
    и создавая их заново.
    Эта функция выполняет следующие действия:
    1. Удаляет все таблицы, определенные в метаданных SQLAlchemy.
    2. Создает новые таблицы на основе текущих моделей.
    :return: словарь с ключом "ok" и значением True
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблица была сброшена и создана заново.")
    return {"ok": True}


@broker.subscriber("create_task")
async def create_task(value: int, session: SessionDep):
    """
    Создает новую задачу в базе данных.
    Эта функция выполняет следующие действия:
    1. Создает новый объект задачи с заданным значением.
    2. Добавляет объект задачи в сессию базы данных.
    3. Сохраняет изменения в базе данных.
    Параметры:
    value (int): Значение, связанное с задачей, которое будет
    сохранено в базе данных.
    session (SessionDep): Сессия базы данных для выполнения операций.
    :return: словарь с ключом "ok" и значением True
    """
    new_task = TaskORM(
        value = value
    )
    session.add(new_task)
    await session.commit()
    logger.info("Была добавлена задача.")
    return {"ok": True}

@broker.subscriber("get_all_task")
async def get_all_task(session: SessionDep):
    """
    Получает все задачи из базы данных.
    Эта функция выполняет следующие действия:
    1. Выполняет запрос к базе данных для получения всех задач.
    2. Преобразует полученные объекты SQLAlchemy в Pydantic модели.
    Параметры:
    session (SessionDep): Сессия базы данных для выполнения операций.
    :return:list[TaskSchema]: Список Pydantic моделей, представляющих все задачи в базе данных.
        """
    query = select(TaskORM)
    result = await session.execute(query)
    task = result.scalars().all()
    logger.info("Был получен список всех задач.")
    return [TaskSchema.model_validate(row, from_attributes = True) for row in task]

@broker.subscriber("get_id_task")
async def get_id_task(index: int, session: SessionDep):
    """
    Получает задачу по заданному идентификатору из базы данных.
    Эта функция выполняет следующие действия:
    1. Выполняет запрос к базе данных для получения задачи с указанным идентификатором.
    2. Преобразует полученный объект SQLAlchemy в Pydantic модель, если задача найдена.
    Параметры:
    index (int): Идентификатор задачи, которую необходимо получить.
    session (SessionDep): Сессия базы данных для выполнения операций.
    Возвращает:
    TaskSchema | dict:
    - Если задача найдена, возвращает Pydantic модель, представляющую задачу.
    - Если задача не найдена, возвращает словарь с сообщением об ошибке.
    """
    query = select(TaskORM).where(TaskORM.id == index)
    result = await session.execute(query)
    task = result.scalars().all()
    if task:
        logger.info("Была найдена задача по ID.")
        return [TaskSchema.model_validate(row, from_attributes = True) for row in task]
    else:
        logger.error("Задача по ID не найдена.")
        return {'message': 'Задачи с таким идентификатором нет.'}


@broker.subscriber("run_task")
@broker.publisher("get_result")
async def run_task(index: int, session: SessionDep):
    query = select(TaskORM).where(TaskORM.id == index)
    result = await session.execute(query)
    task = result.scalars().first()
    if task:
        answer = TaskSchema.model_validate(task, from_attributes = True)
        task.status = 'running'
        task.result = fibonacci(task.value)
        await session.commit()
        await asyncio.sleep(5)
        task.status = 'complete'
        await session.commit()
        logger.info("Задача по ID выполнена.")
        return answer
    else:
        logger.error("Задача по ID не найдена.")
        return {"message": "Задачи с таким идентификатором нет."}


