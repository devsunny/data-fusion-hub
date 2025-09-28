from fastapi import FastAPI
from app.api.v1.endpoints.data_fusion import router
from app.core.mcp_handler import mcp_router

app = FastAPI(title="Data Fusion Hub", version="1.0")

app.include_router(router, prefix="/api/v1/data")
app.include_router(mcp_router, prefix="/mcp")