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