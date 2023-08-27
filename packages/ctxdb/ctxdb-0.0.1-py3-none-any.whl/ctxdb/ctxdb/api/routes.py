from fastapi import FastAPI
from ..core.ctxdb import ContextDB

app = FastAPI()
ctxdb = ContextDB()


@app.post("/contexts")
def add_context():
    ctxdb.add_context()


@app.get("/contexts/{idx}")
def get_context(idx: str):
    ctxdb.get_context(idx)


@app.delete("/contexts/{idx}")
def delete_context(idx: str):
    ctxdb.delete_context(idx)


@app.put("/contexts/{idx}")
def update_context(idx: str):
    ctxdb.update_context(idx)


@app.post("/contexts/query")
def query_context():
    ctxdb.query()
