from pydantic import BaseModel

class TaskAddSchema(BaseModel):
    value: int
    status: str = 'create'
    result: int = 0

class TaskSchema(TaskAddSchema):
    id: int