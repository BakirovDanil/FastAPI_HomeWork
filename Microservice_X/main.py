from fastapi import FastAPI
from Endpoint.methods import tasks, broker, router
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup():
    await broker.connect()

@app.on_event("shutdown")
async def shutdown():
    await broker.close()

app.include_router(tasks)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload = True)