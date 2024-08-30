from fastapi import FastAPI
from .router import book


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my ecommerce books store"}


app.include_router(book.router)


