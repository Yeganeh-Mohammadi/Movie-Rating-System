from app.db.database import SessionLocal
from app.models.models import Director, Genre

def seed():
    db = SessionLocal()
    # اضافه کردن کارگردان نمونه
    if not db.query(Director).filter(Director.name == "Christopher Nolan").first():
        nolan = Director(name="Christopher Nolan", birth_year=1970, description="Sci-fi master")
        db.add(nolan)
    
    # اضافه کردن ژانر نمونه
    if not db.query(Genre).filter(Genre.name == "Action").first():
        action = Genre(name="Action", description="Action movies")
        db.add(action)
    
    db.commit()
    db.close()
    print("داده‌های اولیه با موفقیت اضافه شدند!")

if __name__ == "__main__":
    seed()