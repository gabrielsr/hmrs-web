from . import db
from sqlalchemy import String
from sqlalchemy.orm import  Mapped, mapped_column

# create datatable
class Upload(db.Model):
    __tablename__ = "uploads"

    id:Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(50), nullable=False)
    data: Mapped[bytes] = mapped_column()
 