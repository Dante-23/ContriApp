from fastapi import FastAPI
from random import randrange
from .database import engine, Base
from .routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

contris = [
    {
        "PaidBy": "test@gmail.com",
        "Amount": "500",
        "Name": "Snacks",
        "Contributors": [
            "test@gmail.com",
            "test1@gmail.com",
            "test2@gmail.com",
            "test3@gmail.com"
        ]
    },
    {
        "PaidBy": "test1@gmail.com",
        "Amount": "4000",
        "Name": "Tickets",
        "Contributors": [
            "test@gmail.com",
            "test1@gmail.com"
        ]
    },
    {
        "PaidBy": "test2@gmail.com",
        "Amount": "5000",
        "Name": "Lunch",
        "Contributors": [
            "test@gmail.com",
            "test1@gmail.com"
            "test3@gmail.com"
        ]
    },
    {
        "PaidBy": "test2@gmail.com",
        "Amount": "1000",
        "Name": "Rabdi faluda",
        "Contributors": [
            "test@gmail.com",
            "test1@gmail.com",
            "test2@gmail.com",
            "test3@gmail.com"
        ]
    }
]

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/contri")
def get_all_contri():
    return contris
