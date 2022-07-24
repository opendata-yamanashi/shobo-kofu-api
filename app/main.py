from fastapi import FastAPI
import os
from pathlib import Path

from model import ShoboData
from pydantic import BaseModel, Field
from typing import List

import pandas as pd

FILE_URL = "https://www.city.kofu.yamanashi.jp/joho/opendata/shisetsu/documents/syokasenspot_20200401.xlsx"

FILE_DIR = Path(__file__).absolute().parent.parent / "data"
FILE_NAME = FILE_URL.split("/")[-1]

df = pd.read_csv((FILE_DIR / FILE_NAME).with_suffix(".csv"), header=0)

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
    return df.to_dict("records")

@app.get("/query/", response_model=List[ShoboData])
def do_query(q=None):
    return df.to_dict("records")

class VersionEndpointResponse(BaseModel):
    version: str = Field(None, alias="version")

@app.get("/version/", response_model=VersionEndpointResponse)
def get_version():
    return {"version": "unkown"}