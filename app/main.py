from typing import List

from fastapi import FastAPI
import os

from pydantic import BaseModel, Field
from sqlmodel import select
from db import ShoboData, ShoboDataWithId, get_session


if os.getenv("PYTHON_ENV") == "production":
    root_path = os.getenv("ROOT_PATH", "/")
else:
    root_path = "/"

app = FastAPI(
    title="消防水利施設一覧（消火栓）API",
    root_path=root_path
)

@app.get("/")
def hello():
    return "Hello! Please access /docs"

@app.get("/list/", response_model=List[ShoboData])
def get_data():
    with get_session() as session:
        statement = select(ShoboDataWithId)
        result = session.exec(statement)
        return result.all()

@app.get("/query/", response_model=List[ShoboData])
def do_query(q=None):
    with get_session() as session:
        statement = select(ShoboDataWithId)
        result = session.exec(statement)
        return result.all()

class VersionEndpointResponse(BaseModel):
    version: str = Field(None, alias="version")

@app.get("/version/", response_model=VersionEndpointResponse)
def get_version():
    return {"version": "unkown"}