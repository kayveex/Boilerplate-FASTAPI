# Import semua model di sini agar Alembic Base.metadata mendeteksi semua tabel
from app.core.database import Base
from app.models.item import Item

__all__ = ["Base", "Item"]
