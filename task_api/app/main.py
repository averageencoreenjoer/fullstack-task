from fastapi import FastAPI
from .database import engine, Base
from .routers import tasks
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations with tasks. The main endpoint for creating, retrieving, updating, and deleting tasks.",
    }
]

app = FastAPI(
    title="Task Manager API",
    description="This is a simple but powerful REST API for managing tasks. It's built with FastAPI and SQLAlchemy.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "your-email@example.com",
    },
    openapi_tags=tags_metadata
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)


@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Task API"}
