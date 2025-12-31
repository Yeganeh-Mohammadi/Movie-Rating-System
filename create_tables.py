from app.db.database import engine
from app.models.models import Base

print("در حال ساخت جدول‌ها...")
Base.metadata.create_all(bind=engine)
print("جدول‌ها با موفقیت ساخته شدند!")