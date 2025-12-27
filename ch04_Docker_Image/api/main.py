from fastapi import FastAPI

from api.routers import task,done

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)


# @app.get("/hello")
# async def hello():
#     return {"message": "Hello, FastAPI with Docker!"}

# @app.get("/")
# def read_root():
#     return {"ok": True}

# TODO: add routers and application startup/shutdown logic as needed
