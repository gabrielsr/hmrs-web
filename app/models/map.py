from typing import Optional
from . import db
from . import Upload
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Map(db.Model):
    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    file_id: Mapped[Optional[int]] = mapped_column(ForeignKey("uploads.id"))
    file: Mapped[Upload] = relationship(primaryjoin="Map.file_id == Upload.id", backref="maps")
