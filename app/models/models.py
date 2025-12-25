from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# جدول میانی برای رابطه چند به چند فیلم و ژانر (صفحه 3 و 4 فایل)
movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_year = Column(Integer)
    description = Column(String)
    movies = relationship("Movie", back_populates="director")

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer)
    cast = Column(String)
    director_id = Column(Integer, ForeignKey("directors.id"))
    
    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    ratings = relationship("MovieRating", back_populates="movie", cascade="all, delete-orphan")

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")

class MovieRating(Base):
    __tablename__ = "movie_ratings"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    score = Column(Integer, nullable=False) # باید بین 1 تا 10 باشد
    movie = relationship("Movie", back_populates="ratings")