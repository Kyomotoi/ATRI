from fastapi import FastAPI

# from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router

# from ..data_source import FRONTEND_DIR


app = FastAPI(
    title="Console for ATRI",
    description="A admin UI controller for ATRI",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])

app.include_router(api_router, prefix="/capi")

# app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="Console for ATRI")
