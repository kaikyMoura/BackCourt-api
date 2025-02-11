from fastapi import FastAPI
import uvicorn
from app.routes.articles import router

app = FastAPI(title="Basketball Advanced Stats", description="API for basketball advanced stats", version="1.0")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)