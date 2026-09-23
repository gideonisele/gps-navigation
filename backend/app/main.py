from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.locations import router as locations_router


app = FastAPI(
    title="GPS Navigation API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(locations_router)


@app.get("/api/v1/health")
def health():

    return {
        "status": "healthy",
        "service": "gps-navigation-api",
        "version": "0.1.0",
    }