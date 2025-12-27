from sqlalchemy.orm import Session
from app.repositories.movie_repository import MovieRepository
from app.schemas.movie import RatingCreate
from app.models.models import Genre, Movie
class MovieService:

    @staticmethod
    def list_movies(
        db: Session,
        page: int,
        page_size: int,
        title: str | None,
        release_year: int | None,
        genre: str | None,
    ):
        skip = (page - 1) * page_size

        movies, total_items = MovieRepository.get_movies(
            db=db,
            title=title,
            release_year=release_year,
            genre=genre,
            skip=skip,
            limit=page_size
        )

        items = []
        for movie in movies:
            items.append({
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "director": {
                    "id": movie.director.id if movie.director else None,
                    "name": movie.director.name if movie.director else None
                },
                "genres": [g.name for g in movie.genres],
                "average_rating": movie.average_rating
            })

        return {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "items": items
        }

    @staticmethod
    def add_movie(db: Session, movie_data):
        return MovieRepository.create(db, movie_data)

    @staticmethod
    def add_rating(db: Session, rating_data: RatingCreate, movie_id: int):
        return MovieRepository.create_rating(db, rating_data, movie_id)

    @staticmethod
    def get_movie_by_id(db: Session, movie_id: int):
        return MovieRepository.get_movie_by_id(db, movie_id)
    
    @staticmethod
    def delete_movie(db: Session, movie_id: int):
        movie = db.query(Movie).filter(Movie.id == movie_id).first()

        if not movie:
            return None

        db.delete(movie)
        db.commit()
        return True

    @staticmethod
    def update_movie(
        db: Session,
        movie_id: int,
        movie_data
    ):
        movie = db.query(Movie).filter(Movie.id == movie_id).first()

        if not movie:
            return None

        if movie_data.title is not None:
            movie.title = movie_data.title

        if movie_data.release_year is not None:
            movie.release_year = movie_data.release_year

        if movie_data.cast is not None:
            movie.cast = movie_data.cast

        if movie_data.genres is not None:
            genres = db.query(Genre).filter(
                Genre.id.in_(movie_data.genres)
            ).all()
            movie.genres = genres

        db.commit()
        db.refresh(movie)
        return movie
