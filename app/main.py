from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD API",
    description="This API allows users to perform CRUD operations on items stored in an SQLite database.",
    version="1.0.0",
    contact={
        "name": "Christopher Lim",
        "email": "toffer.lim87@gmail.com",
    },
)

app.include_router(router)
