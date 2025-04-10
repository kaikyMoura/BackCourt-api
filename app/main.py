from fastapi import FastAPI
import uvicorn
from app.routes import router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="Backcourt API", description="API for the Backcourt application", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["X-Custom-Header"],
)

app.include_router(router, prefix='/api/v1')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)