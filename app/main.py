from data import Kofu_shobo
from fastapi import FastAPI

data = Kofu_shobo()
data.create_df()

app = FastAPI()

@app.get("/")
def hello():
    return "Hello! Please access /docs"

@app.get("/list/")
def get_data():
    return data.df.T

@app.get("/query/")
def do_query(q=None):
    return data.query(q).T

@app.get("/version/")
def get_version():
    return {"version": data.get_version()}