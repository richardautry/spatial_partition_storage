from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, SQLModel, Session, create_engine, select

app = FastAPI()


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


engine = create_engine("postgresql://postgres:postgres@postgres")

SQLModel.metadata.create_all(engine)

hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")


with Session(engine) as session:
    session.add(hero_1)
    session.commit()


@app.get("/")
def read_root():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        hero = session.exec(statement).first()
        print(hero)
        return hero


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
