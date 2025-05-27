from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class AnonymousUser(Base):
    id: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Связи
    history: Mapped[list["UserCityHistory"]] = relationship(
        back_populates="user", cascade="all, delete", passive_deletes=True
    )
