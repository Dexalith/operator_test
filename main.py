from fastapi import FastAPI
import uvicorn

from db.config import app_config
from app.api import router

app = FastAPI(
    title="Lead Distribution CRM",
    description="Асинхронный CRM для распределения лидов между операторами",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.include_router(router, prefix="/api/v1", tags=["crm"])


@app.get("/")
async def root():
    return {"message": "Lead Distribution CRM API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "SQLite"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_config.app_host,
        port=app_config.app_port,
        reload=True,
    )