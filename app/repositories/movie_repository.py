from sqlalchemy.orm import Session
from app.models.models import Movie, Genre, MovieRating
from app.schemas.movie import MovieCreate, RatingCreate 

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
    
    @staticmethod
    def create_rating(db: Session, rating_data: RatingCreate, movie_id: int):
        db_rating = MovieRating(
            score=rating_data.score,
            comment=rating_data.comment,
            user_id=rating_data.user_id,
            movie_id=movie_id
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating

    @staticmethod
    def get_movie_by_id(db: Session, movie_id: int): # برای چک کردن وجود فیلم لازم است
        return db.query(Movie).filter(Movie.id == movie_id).first()