from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.services.movie_service import MovieService
from app.schemas.movie import (
    PaginatedMovieResponse,
    MovieCreate,
    RatingCreate,
    MovieUpdate,
    StandardResponse
)
from app.core.logging_config import get_logger


router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])

movies_logger = get_logger("movies")
ratings_logger = get_logger("ratings")


@router.get("/", response_model=PaginatedMovieResponse)
def read_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    title: Optional[str] = None,
    release_year: Optional[int] = None,
    genre: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # INFO log — شروع درخواست لیست فیلم‌ها
    movies_logger.info(
        "Fetching movie list",
        extra={
            "page": page,
            "page_size": page_size,
            "title": title,
            "release_year": release_year,
            "genre": genre,
            "route": "/api/v1/movies"
        }
    )

    result = MovieService.list_movies(db, page, page_size, title, release_year, genre)

    # INFO log — پایان موفق
    movies_logger.info(
        "Movie list fetched successfully",
        extra={"total_items": result.get("total_items")}
    )

    return {"status": "success", "data": result}


@router.get("/{movie_id}", response_model=StandardResponse)
def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie = MovieService.get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="فیلم پیدا نشد")
    return {"status": "success", "data": movie}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return {"status": "success", "data": MovieService.add_movie(db, movie)}


@router.post("/{movie_id}/ratings", status_code=status.HTTP_201_CREATED)
def rate_movie(movie_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    # WARNING — امتیاز نامعتبر
    if rating.score < 1 or rating.score > 5:
        ratings_logger.warning(
            "Invalid rating value",
            extra={
                "movie_id": movie_id,
                "rating": rating.score,
                "route": f"/api/v1/movies/{movie_id}/ratings"
            }
        )
        raise HTTPException(status_code=422, detail="Invalid rating value")

    # INFO — ثبت امتیاز
    ratings_logger.info(
        "Rating movie",
        extra={
            "movie_id": movie_id,
            "rating": rating.score,
            "route": f"/api/v1/movies/{movie_id}/ratings"
        }
    )

    try:
        result = MovieService.add_rating(db, rating, movie_id)

        # INFO — ثبت موفق
        ratings_logger.info(
            "Rating saved successfully",
            extra={"movie_id": movie_id, "rating": rating.score}
        )

        return {"status": "success", "data": result}

    except Exception:
        # ERROR — خطای سیستمی با stacktrace
        ratings_logger.error(
            "Failed to save rating",
            extra={"movie_id": movie_id, "rating": rating.score},
            exc_info=True
        )
        raise


@router.put("/{movie_id}", response_model=StandardResponse)
def update_movie(movie_id: int, movie_data: MovieUpdate, db: Session = Depends(get_db)):
    movie = MovieService.update_movie(db, movie_id, movie_data)
    if not movie:
        raise HTTPException(status_code=404, detail="فیلم پیدا نشد")
    return {"status": "success", "data": movie}


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    if not MovieService.delete_movie(db, movie_id):
        raise HTTPException(status_code=404, detail="فیلم پیدا نشد")
    return None