from sqlalchemy.orm import Session
from app.models.models import Movie, Genre, MovieRating
from app.schemas.movie import MovieCreate, RatingCreate 
from sqlalchemy import func

class MovieRepository:
    @staticmethod
    def get_movies(
        db: Session, 
        title: str = None, 
        year: int = None, 
        genre: str = None, 
        skip: int = 0, 
        limit: int = 10
    ):
        """دریافت فیلم‌ها با فیلتر و صفحه‌بندی"""
        
        # Query اصلی با JOIN به director و genres
        query = db.query(Movie).options(
            joinedload(Movie.director),
            joinedload(Movie.genres)
        )
        
        # فیلتر عنوان (جستجوی بخشی - case insensitive)
        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        
        # فیلتر سال
        if year:
            query = query.filter(Movie.release_year == year)
        
        # فیلتر ژانر
        if genre:
            query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre}%"))
        
        # محاسبه total قبل از pagination
        total_items = query.count()
        
        # اعمال pagination
        movies = query.offset(skip).limit(limit).all()
        
        # محاسبه میانگین امتیاز برای هر فیلم
        for movie in movies:
            avg_score = db.query(func.avg(MovieRating.score)).filter(
                MovieRating.movie_id == movie.id
            ).scalar()
            movie.average_rating = round(avg_score, 1) if avg_score else None
        
        return movies, total_items
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
    def get_movie_by_id(db: Session, movie_id: int):
        # پیدا کردن فیلم
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        
        if movie:
            # محاسبه میانگین امتیازات از جدول MovieRating
            avg_score = db.query(func.avg(MovieRating.score)).filter(MovieRating.movie_id == movie_id).scalar()
            # اضافه کردن مقدار به آبجکت فیلم (اسکیما خودش این رو میگیره و نشون میده)
            movie.average_rating = round(avg_score, 1) if avg_score else 0.0
            
        return movie
