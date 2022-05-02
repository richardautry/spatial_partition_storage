from typing import Optional

from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine, select
from app.models.objects import Box

app = FastAPI()


engine = create_engine("postgresql://postgres:postgres@postgres")

SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "world"}


@app.get("/boxes/{box_id}")
def read_item(box_id: int, q: Optional[str] = None):
    return {"box_id": box_id, "q": q}


@app.get("/boxes/")
def get_boxes():
    with Session(engine) as session:
        statement = select(Box)
        results = session.exec(statement).all()

    return results


@app.post("/boxes/")
def post_box(box: Box):
    with Session(engine) as session:
        session.add(box)
        session.commit()
        session.refresh(box)

    return box
