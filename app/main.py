from pydantic import UUID4
from typing import List, Union

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from app.models.objects import (
    Box,
    X,
    Y,
    Z,
    BoxReadWithValues,
    XReadWithBoxes,
    ZReadWithBoxes,
    XBoxLink,
    YBoxLink,
    ZBoxLink,
    BoxRead
)
from app.utils import get_dimension_values, DimensionQuery
from app.cache import redis_client

app = FastAPI()

engine = create_engine("postgresql://postgres:postgres@postgres", echo=True)

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# TODO: Env Var to set fidelity/sampling frequency
fidelity = 10

x_query = DimensionQuery(
    Model=X,
    LinkModel=XBoxLink,
    fidelity=fidelity
)

y_query = DimensionQuery(
    Model=Y,
    LinkModel=YBoxLink,
    fidelity=fidelity
)

z_query = DimensionQuery(
    Model=Z,
    LinkModel=ZBoxLink,
    fidelity=fidelity
)


# TODO: Add feature to search for all boxes near input box
# TODO: Add limit query param
@app.get("/boxes/", response_model=List[BoxRead])
def get_boxes(
    *,
    session: Session = Depends(get_session),
    x: Union[int, None] = None,
    x_gte: Union[int, None] = None,
    x_lte: Union[int, None] = None,
    y: Union[int, None] = None,
    y_gte: Union[int, None] = None,
    y_lte: Union[int, None] = None,
    z: Union[int, None] = None,
    z_gte: Union[int, None] = None,
    z_lte: Union[int, None] = None,
):
    statement = select(Box)

    statement = x_query.get_full_statement(
        eq_value=x,
        ge_value=x_gte,
        le_value=x_lte,
        statement=statement
    )

    statement = y_query.get_full_statement(
        eq_value=y,
        ge_value=y_gte,
        le_value=y_lte,
        statement=statement
    )

    statement = z_query.get_full_statement(
        eq_value=z,
        ge_value=z_gte,
        le_value=z_lte,
        statement=statement
    )

    results = session.exec(statement).all()
    return results


@app.get("/boxes/{box_id}", response_model=BoxReadWithValues)
def get_box(*, session: Session = Depends(get_session), box_id: UUID4):
    box = session.get(Box, box_id)
    if not box:
        raise HTTPException(status_code=404, detail="Box not found.")
    return box


@app.post("/boxes/", response_model=BoxReadWithValues)
def post_box(*, session: Session = Depends(get_session), box: Box):
    # with Session(engine) as session:
    # TODO: Function for creating y, z lookups
    box.x_values = get_dimension_values(
        session=session,
        model=X,
        min_val=int(box.x_min),
        max_val=int(box.x_max),
        step_size=fidelity
    )
    box.y_values = get_dimension_values(
        session=session,
        model=Y,
        min_val=int(box.y_min),
        max_val=int(box.y_max),
        step_size=fidelity
    )
    box.z_values = get_dimension_values(
        session=session,
        model=Z,
        min_val=int(box.z_min),
        max_val=int(box.z_max),
        step_size=fidelity
    )
    session.add(box)
    session.commit()
    session.refresh(box)
    return box


# TODO: Query params?
@app.get("/x/", response_model=List[XReadWithBoxes])
def get_x(*, session: Session = Depends(get_session)):
    statement = select(X)
    results = session.exec(statement).all()

    return results


@app.get("/z/", response_model=List[ZReadWithBoxes])
def get_z(*, session: Session = Depends(get_session)):
    statement = select(Z)
    results = session.exec(statement).all()

    return results
