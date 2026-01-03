from app.db.database import SessionLocal
from app.models.models import Director, Genre

def seed():
    db = SessionLocal()

    # کارگردان‌ها
    directors = [
        {"name": "Christopher Nolan", "birth_year": 1970, "description": "Sci-fi master"},
        {"name": "Quentin Tarantino", "birth_year": 1963, "description": "Cult films"}
    ]
    for d in directors:
        if not db.query(Director).filter(Director.name == d["name"]).first():
            db.add(Director(**d))

    # ژانرها
    genres = [
        {"name": "Action", "description": "Action movies"},
        {"name": "Sci-Fi", "description": "Science fiction"},
        {"name": "Drama", "description": "Dramatic movies"},
        {"name": "Thriller", "description": "Thriller movies"}
    ]
    for g in genres:
        if not db.query(Genre).filter(Genre.name == g["name"]).first():
            db.add(Genre(**g))

    db.commit()
    db.close()
    print("Seed data added successfully!")

if __name__ == "__main__":
    seed()
