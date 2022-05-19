from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from pydantic import UUID4
from uuid import uuid4


# TODO: Experiment with using one master Coordinates table
# i.e. dimension ("x", "y", etc.), val (0, 10, 20, ...) and CoordinatesBoxLink
class XBoxLink(SQLModel, table=True):
    box_id: Optional[UUID4] = Field(default=None, foreign_key="box.id", primary_key=True)
    x_id: Optional[int] = Field(default=None, foreign_key="x.id", primary_key=True)


class YBoxLink(SQLModel, table=True):
    box_id: Optional[UUID4] = Field(default=None, foreign_key="box.id", primary_key=True)
    y_id: Optional[int] = Field(default=None, foreign_key="y.id", primary_key=True)


class ZBoxLink(SQLModel, table=True):
    box_id: Optional[UUID4] = Field(default=None, foreign_key="box.id", primary_key=True)
    z_id: Optional[int] = Field(default=None, foreign_key="z.id", primary_key=True)


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
    y_values: List["Y"] = Relationship(back_populates="boxes", link_model=YBoxLink)
    z_values: List["Z"] = Relationship(back_populates="boxes", link_model=ZBoxLink)


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


class XReadWithBoxes(XRead):
    boxes: List[BoxRead] = []


class YBase(SQLModel):
    pass


class Y(YBase, table=True):
    id: int = Field(default=None, primary_key=True)
    boxes: List[Box] = Relationship(back_populates="y_values", link_model=YBoxLink)


class YRead(YBase):
    id: int


class ZBase(SQLModel):
    pass


class Z(ZBase, table=True):
    id: int = Field(default=None, primary_key=True)
    boxes: List[Box] = Relationship(back_populates="z_values", link_model=ZBoxLink)


class ZRead(ZBase):
    id: int


class BoxReadWithValues(BoxRead):
    x_values: List[XRead] = []
    y_values:  List[YRead] = []
    z_values: List[ZRead] = []
