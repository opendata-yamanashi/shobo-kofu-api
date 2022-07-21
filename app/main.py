from data import Kofu_shobo
from fastapi import FastAPI
import os

from model import ShoboData
from pydantic import BaseModel, Field
from typing import List

data = Kofu_shobo()
data.create_df()

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
    return data.df.to_dict("records")

@app.get("/query/", response_model=List[ShoboData])
def do_query(q=None):
    return data.query(q).to_dict("records")

class VersionEndpointResponse(BaseModel):
    version: str = Field(None, alias="version")

@app.get("/version/", response_model=VersionEndpointResponse)
def get_version():
    return {"version": data.get_version()}