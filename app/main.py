from fastapi import FastAPI

from .routers import projects

app = FastAPI()
app.include_router(projects.router, prefix="/project")


@app.get("/")
async def index():
    return {"message": "Welcome to my solution to the Orbify backend task!"}
