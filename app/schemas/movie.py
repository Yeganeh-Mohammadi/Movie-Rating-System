from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class DirectorInMovie(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    title: str
    release_year: int
    cast: str

class MovieCreate(MovieBase):
    director_id: int
    genre_ids: List[int]

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    cast: Optional[str] = None
    genres: Optional[List[int]] = None

class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=10) 
    user_id: Optional[int] = None
    comment: Optional[str] = None

class RatingResponse(BaseModel):
    id: int
    movie_id: int
    score: int
    class Config:
        from_attributes = True

class MovieResponse(BaseModel):
    id: int
    title: str
    release_year: int
    cast: str
    director: DirectorInMovie
    genres: List[str]
    average_rating: float = 0.0
    ratings_count: int = 0

    @field_validator('genres', mode='before')
    @classmethod
    def transform_genres(cls, v):
        # تبدیل خودکار آبجکت ژانر به نام رشته‌ای برای جلوگیری از ارور 500
        if isinstance(v, list) and len(v) > 0 and not isinstance(v[0], str):
            return [g.name for g in v]
        return v

    class Config:
        from_attributes = True

class PaginatedMoviesData(BaseModel):
    page: int
    page_size: int
    total_items: int
    items: List[MovieResponse]

class PaginatedMovieResponse(BaseModel):
    status: str = "success"
    data: PaginatedMoviesData

class StandardResponse(BaseModel):
    status: str = "success"
    data: MovieResponse
