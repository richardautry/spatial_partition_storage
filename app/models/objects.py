from typing import Optional

from sqlmodel import SQLModel, Field
from pydantic import UUID4
from uuid import uuid4


class Box(SQLModel, table=True):
    id: Optional[UUID4] = Field(default=uuid4, primary_key=True)
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    z_min: float
    z_max: float
