from fastapi import FastAPI
from src.routers.main import include

app = FastAPI()
include(app)
