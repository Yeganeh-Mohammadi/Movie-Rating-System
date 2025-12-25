from sqlalchemy.orm import Session
from app.models.models import Movie, Genre
from app.schemas.movie import MovieCreate

class MovieRepository:
    @staticmethod
    def get_movies(db: Session, title: str = None, year: int = None, genre: str = None, skip: int = 0, limit: int = 10):
        query = db.query(Movie)
        if title:
            query = query.filter(Movie.title.contains(title))
        if year:
            query = query.filter(Movie.release_year == year)
        if genre:
            query = query.join(Movie.genres).filter(Genre.name == genre)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, movie_data: MovieCreate):
        db_movie = Movie(
            title=movie_data.title,
            release_year=movie_data.release_year,
            cast=movie_data.cast,
            director_id=movie_data.director_id
        )
        if movie_data.genre_ids:
            genres = db.query(Genre).filter(Genre.id.in_(movie_data.genre_ids)).all()
            db_movie.genres = genres
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie