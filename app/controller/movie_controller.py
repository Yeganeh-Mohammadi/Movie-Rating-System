from fastapi import APIRouter, Depends, Query, status, HTTPException 
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.movie_service import MovieService
from app.schemas.movie import PaginatedMovieResponse, MovieCreate, RatingCreate, MovieUpdate, StandardResponse
from typing import Optional

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])

@router.get("/", response_model=PaginatedMovieResponse)
def read_movies(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1), title: Optional[str] = None, release_year: Optional[int] = None, genre: Optional[str] = None, db: Session = Depends(get_db)):
    result = MovieService.list_movies(db, page, page_size, title, release_year, genre)
    return {"status": "success", "data": result}

@router.get("/{movie_id}", response_model=StandardResponse)
def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie = MovieService.get_movie_by_id(db, movie_id)
    if not movie: raise HTTPException(status_code=404, detail="فیلم پیدا نشد")
    return {"status": "success", "data": movie}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return {"status": "success", "data": MovieService.add_movie(db, movie)}

@router.post("/{movie_id}/ratings", status_code=status.HTTP_201_CREATED)
def rate_movie(movie_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    return {"status": "success", "data": MovieService.add_rating(db, rating, movie_id)}

@router.put("/{movie_id}", response_model=StandardResponse)
def update_movie(movie_id: int, movie_data: MovieUpdate, db: Session = Depends(get_db)):
    movie = MovieService.update_movie(db, movie_id, movie_data)
    if not movie: raise HTTPException(status_code=404, detail="فیلم پیدا نشد")
    return {"status": "success", "data": movie}

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    if not MovieService.delete_movie(db, movie_id): raise HTTPException(status_code=404, detail="فیلم پیدا نشد")
    return None
