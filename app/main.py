import contextlib
import os
from fastapi import FastAPI
import uvicorn
from app.config.nba_api_config import configure_nba_api
from app.routes import router
from starlette.middleware.cors import CORSMiddleware


# Link to the docs: https://fastapi.tiangolo.com/advanced/events/?h=contextlib#async-context-manager
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    configure_nba_api()
    print("✅ Backcourt API online")
    yield
    print("🛑 Backcourt API offline")


app = FastAPI(lifespan=lifespan)


app = FastAPI(
    title="Backcourt API",
    description="API for the Backcourt application",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["X-Custom-Header"],
)

app.include_router(router, prefix="/v1")

@app.get("/health")
async def health_check():
    try:
        return {"status": "healthy", "message": "✅ Backcourt API is running"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"🛑 Backcourt API is offline"}


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Backcourt API",
        "details": "Acess the documentation at /docs",
    }


if __name__ == "__main__":
    configure_nba_api()
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 8080))
