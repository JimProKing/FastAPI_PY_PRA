from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"ok": True}

# TODO: add routers and application startup/shutdown logic as needed
