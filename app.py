from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

from routers.analyze import router as analyze_router
app.include_router(analyze_router, tags=["analyze"], prefix="/api/v1")