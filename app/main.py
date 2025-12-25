from fastapi import FastAPI
from app.controller import movie_controller  # وارد کردن کنترلر فیلم‌ها

app = FastAPI(title="Movie Rating System API")

# ثبت کردن مسیرهای فیلم در برنامه اصلی
app.include_router(movie_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Rating System Phase 1"}