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