from fastapi import FastAPI
from app.controller import movie_controller

app = FastAPI()

app.include_router(movie_controller.router)

