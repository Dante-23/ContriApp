from fastapi import FastAPI
from random import randrange
from .database import engine, Base
from .routers import users, expenditures

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(expenditures.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
