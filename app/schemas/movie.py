from pydantic import BaseModel, Field
from typing import List, Optional

class MovieBase(BaseModel):
    title: str
    release_year: int
    cast: str
    director_id: int

class MovieCreate(MovieBase):
    genre_ids: List[int] # لیستی از آی‌دی ژانرها برای ثبت در جدول واسط

class MovieResponse(MovieBase):
    id: int
    # فیلد زیر برای نمایش میانگین نمرات اضافه می‌شود
    average_rating: Optional[float] = Field(0.0, description="میانگین امتیازات فیلم")

    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=5, description="امتیاز باید بین 1 تا 5 باشد")
    comment: Optional[str] = None
    user_id: Optional[int] = None

# اسکیمای خروجی برای نمایش امتیاز
class RatingResponse(RatingCreate):
    id: int
    movie_id: int

    class Config:
        from_attributes = True

class DirectorInMovie(BaseModel):
    """اسکیمای کارگردان برای نمایش در لیست فیلم‌ها"""
    id: int
    name: str

    class Config:
        from_attributes = True

class MovieListItem(BaseModel):
    """اسکیمای هر فیلم در لیست"""
    id: int
    title: str
    release_year: int
    director: DirectorInMovie
    genres: List[str]  # فقط اسم ژانرها
    average_rating: Optional[float] = None

    class Config:
        from_attributes = True

class PaginatedMovieResponse(BaseModel):
    status: str
    data: List[MovieResponse]
    page: int
    page_size: int
    total: int

class ErrorResponse(BaseModel):
    """پاسخ خطا"""
    status: str = "failure"
    error: dict

class PaginatedMoviesData(BaseModel):
    page: int
    page_size: int
    total_items: int
    items: List[MovieResponse]
    
class MovieUpdate(BaseModel):
    title: Optional[str]
    release_year: Optional[int]
    cast: Optional[str]
    genres: Optional[List[int]]
