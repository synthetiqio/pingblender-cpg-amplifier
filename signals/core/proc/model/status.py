from typing import Literal 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Control(DeclarativeBase):
    pass

Status = Literal['Pending', 'Processed', 'Reviewed', 'Complete']

class Status(Control):
    process_status: Mapped[Status]