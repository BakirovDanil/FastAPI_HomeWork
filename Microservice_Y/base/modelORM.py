from sqlalchemy.orm import Mapped, mapped_column
from base.db import Base

class TaskORM(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key = True)
    value: Mapped[int] = mapped_column(default = None)
    status: Mapped[str] = mapped_column(default = 'create')
    result: Mapped[int] = mapped_column(default = 0)