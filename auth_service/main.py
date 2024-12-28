from fastapi import FastAPI

from src.routers.main import include_routers

app = FastAPI()
include_routers(app)
