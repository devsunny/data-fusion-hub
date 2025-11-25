"""
Data Fusion Hub Service - Main Application Entry Point
"""

from fastapi import FastAPI
from app.api.v1 import datadomains, dataconnectors, dataobjects, users, roles, auth
from app.api.v1.routes.user_role_requests import router as user_role_requests_router
from app.api.v1.routes.role_approver_relationships import (
    router as role_approver_relationships_router,
)
from app.core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Data Fusion Hub Service",
    description="API for managing data domains, connectors, and objects in the Data Fusion Hub ecosystem",
    version="1.0.0",
)

# Include API routers
app.include_router(datadomains.router)
app.include_router(dataconnectors.router)
app.include_router(dataobjects.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(auth.router)
app.include_router(user_role_requests_router)
app.include_router(role_approver_relationships_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Data Fusion Hub Service API"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)