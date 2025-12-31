from sqlalchemy.orm import Session
from app.repositories.movie_repository import MovieRepository
from app.schemas.movie import RatingCreate
from app.models.models import Genre, Movie

class MovieService:

    @staticmethod
    def list_movies(db: Session, page: int, page_size: int, title: str | None, release_year: int | None, genre: str | None):
        skip = (page - 1) * page_size
        movies, total_items = MovieRepository.get_movies(db, title, release_year, genre, skip, page_size)
        return {"page": page, "page_size": page_size, "total_items": total_items, "items": movies}

    @staticmethod
    def add_movie(db: Session, movie_data):
        return MovieRepository.create(db, movie_data)

    @staticmethod
    def add_rating(db: Session, rating_data, movie_id: int):
        return MovieRepository.create_rating(db, rating_data, movie_id)

    @staticmethod
    def get_movie_by_id(db: Session, movie_id: int):
        return MovieRepository.get_movie_by_id(db, movie_id)
    
    @staticmethod
    def delete_movie(db: Session, movie_id: int):
        movie = db.query(Movie).filter(Movie.id == movie_id).first()

        if not movie:
            return False
        db.delete(movie)
        db.commit()
        return True

    @staticmethod
    def update_movie(db: Session, movie_id: int, movie_data):
        movie = MovieRepository.get_movie_by_id(db, movie_id)
        if not movie: return None
        for key, value in movie_data.dict(exclude_unset=True).items():
            if key == 'genres' and value is not None:
                movie.genres = db.query(Genre).filter(Genre.id.in_(value)).all()
            else:
                setattr(movie, key, value)
        db.commit()
        db.refresh(movie)
        return movie
