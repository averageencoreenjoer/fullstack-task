from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, json_schema_extra={'example': "Buy groceries"})
    description: Optional[str] = Field(None, json_schema_extra={'example': "Milk, bread, and eggs"})
    status: TaskStatus = Field(default=TaskStatus.pending, json_schema_extra={'example': "pending"})


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, json_schema_extra={'example': "Finish the report"})
    description: Optional[str] = Field(None, json_schema_extra={'example': "Final draft of the Q3 sales report"})
    status: Optional[TaskStatus] = Field(None, json_schema_extra={'example': "in_progress"})


class Task(TaskBase):
    id: int = Field(..., json_schema_extra={'example': 123})
    created_at: datetime = Field(..., json_schema_extra={'example': "2025-09-29T10:00:00.000Z"})

    model_config = ConfigDict(from_attributes=True)
    