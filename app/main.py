from data import Kofu_shobo
from fastapi import FastAPI
import os

data = Kofu_shobo()
data.create_df()

root_path = os.getenv("ROOT_PATH", "")
app = FastAPI(
    title="消防水利施設一覧（消火栓）API",
    root_path=root_path
)

@app.get("/")
def hello():
    return "Hello! Please access /docs"

@app.get("/list/")
def get_data():
    return data.df.to_dict("records")

@app.get("/query/")
def do_query(q=None):
    return data.query(q).to_dict("records")

@app.get("/version/")
def get_version():
    return {"version": data.get_version()}