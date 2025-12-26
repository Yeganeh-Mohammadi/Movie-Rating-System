from fastapi import APIRouter, Depends, Query, status, HTTPException 
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.movie_service import MovieService
from app.schemas.movie import MovieResponse, MovieCreate, RatingCreate, RatingResponse 
from app.models.models import Movie 
from typing import List, Optional

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/", response_model=List[MovieResponse])
def read_movies(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    title: Optional[str] = None,
    year: Optional[int] = None,
    genre: Optional[str] = None,
    db: Session = Depends(get_db)):
    return MovieService.list_movies(db, page, size, title, year, genre)

@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return MovieService.add_movie(db, movie)

@router.post("/{movie_id}/ratings", response_model=RatingResponse)
def rate_movie(movie_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    # چک کردن وجود فیلم
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="فیلم مورد نظر پیدا نشد")
    
    # فراخوانی از طریق سرویس
    return MovieService.add_rating(db=db, rating_data=rating, movie_id=movie_id)