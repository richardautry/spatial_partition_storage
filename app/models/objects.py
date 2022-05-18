from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from uuid import uuid4


# TODO: Many to Many link between box and x
class XBoxLink(SQLModel, table=True):
    box_id: Optional[UUID4] = Field(default=None, foreign_key="box.id", primary_key=True)
    x_id: Optional[int] = Field(default=None, foreign_key="x.id", primary_key=True)


class BoxBase(SQLModel):
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    z_min: float
    z_max: float


class Box(BoxBase, table=True):
    id: Optional[UUID4] = Field(default=uuid4, primary_key=True)

    x_values: List["X"] = Relationship(back_populates="boxes", link_model=XBoxLink)


class BoxCreate(BoxBase):
    pass


class BoxRead(BoxBase):
    id: UUID4


class XBase(SQLModel):
    pass


class X(XBase, table=True):
    id: int = Field(default=None, primary_key=True)
    boxes: List[Box] = Relationship(back_populates="x_values", link_model=XBoxLink)


class XRead(XBase):
    id: int


class BoxReadWithX(BoxRead):
    x_values: List[XRead] = []


class XReadWithBoxes(XRead):
    boxes: List[BoxRead] = []





# TODO: Dimension lookup table for y

# TODO: Dimension lookup table for z

# TODO: Many to Many link between box and y
# TODO: Many to Many link between box and z
