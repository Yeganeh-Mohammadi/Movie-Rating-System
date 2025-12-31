from fastapi import FastAPI
from app.controller import movie_controller
from app.db.database import Base, engine
from app.models.models import *

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(movie_controller.router)


