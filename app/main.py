from fastapi import FastAPI

from app.database import Base, engine
from app.models import task, user
from app.routers import admin, auth, tasks


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A layered FastAPI project with PostgreSQL, JWT auth, and task CRUD.",
    version="1.0.0",
)

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(tasks.router, prefix=API_PREFIX)
app.include_router(admin.router, prefix=API_PREFIX)


@app.get("/")
def root():
    return {"message": "Task Manager API is running."}
