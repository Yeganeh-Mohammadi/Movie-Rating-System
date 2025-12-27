from fastapi import APIRouter, Depends, Query, status, HTTPException 
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.movie_service import MovieService
from app.schemas.movie import MovieResponse, MovieCreate, PaginatedMovieResponse, RatingCreate, RatingResponse 
from app.models.models import Movie 
from typing import List, Optional
from app.schemas.movie import MovieUpdate

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/", response_model=PaginatedMovieResponse)
def read_movies(
    page: int = Query(1, ge=1, description="شماره صفحه"),
    page_size: int = Query(10, ge=1, le=100, description="تعداد آیتم در هر صفحه"),
    title: Optional[str] = Query(None, description="جستجو در عنوان فیلم"),
    release_year: Optional[int] = Query(None, ge=1800, le=2100, description="سال انتشار"),
    genre: Optional[str] = Query(None, description="فیلتر بر اساس ژانر"),
    db: Session = Depends(get_db)
):
    try:
        result = MovieService.list_movies(
            db, page, page_size, title, release_year, genre
        )
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "failure",
                "error": {
                    "code": 500,
                    "message": str(e)
                }
            }
        )
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

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie = MovieService.get_movie_by_id(db, movie_id) 
    if not movie:
        raise HTTPException(status_code=404, detail="فیلم پیدا نشد")
    return movie

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    deleted = MovieService.delete_movie(db, movie_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "failure",
                "error": {
                    "code": 404,
                    "message": "Movie not found"
                }
            }
        )
@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie_data: MovieUpdate,
    db: Session = Depends(get_db)
):
    movie = MovieService.update_movie(db, movie_id, movie_data)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "failure",
                "error": {
                    "code": 404,
                    "message": "Movie not found"
                }
            }
        )

    return {
        "status": "success",
        "data": movie
    }