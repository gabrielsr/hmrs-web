from typing import Optional
from . import db
from sqlalchemy import ForeignKey, String
from ..auth.principal import Principal
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Profile(db.Model):
    __tablename__ = "profiles"

    id:Mapped[int] = mapped_column(primary_key=True)
    principal_id:Mapped[int] = mapped_column(ForeignKey(Principal.id), unique=True) #*one-to-one
    principal: Mapped[Principal] = relationship(back_populates="me")

    name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(80))
    picture: Mapped[Optional[str]] = mapped_column(String(80))
    bio: Mapped[Optional[str]] = mapped_column(String(300))

    @property
    def username(self):
        if not self.principal:
            return 'not loaded'
        return self.principal.username

    def __repr__(self):
        return f'Profile ({self.id}, {self.name}, {self.email})'




