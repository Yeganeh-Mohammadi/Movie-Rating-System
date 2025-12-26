from sqlalchemy.orm import Session
from app.repositories.movie_repository import MovieRepository
from app.schemas.movie import MovieCreate, RatingCreate 

class MovieService:
    @staticmethod
    def list_movies(db: Session, page: int, size: int, title: str, year: int, genre: str):
        skip = (page - 1) * size
        return MovieRepository.get_movies(db, title, year, genre, skip, size)

    @staticmethod
    def add_movie(db: Session, movie_data):
        return MovieRepository.create(db, movie_data)
    
    @staticmethod
    def add_rating(db: Session, rating_data: RatingCreate, movie_id: int):
        return MovieRepository.create_rating(db, rating_data, movie_id)
    
    @staticmethod
    def get_movie_by_id(db: Session, movie_id: int):
        return MovieRepository.get_movie_by_id(db, movie_id)