from sqlalchemy.orm import Session
from app.repositories.movie_repository import MovieRepository

class MovieService:
    @staticmethod
    def list_movies(db: Session, page: int, size: int, title: str, year: int, genre: str):
        skip = (page - 1) * size
        return MovieRepository.get_movies(db, title, year, genre, skip, size)

    @staticmethod
    def add_movie(db: Session, movie_data):
        return MovieRepository.create(db, movie_data)