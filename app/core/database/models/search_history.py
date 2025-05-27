from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from app.core.database import AnonymousUser, City


class UserCityHistory(Base, IntIdPkMixin):
    user_id: Mapped[str] = mapped_column(
        ForeignKey("anonymous_users.id", ondelete="CASCADE"), nullable=False
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Cвязи
    user: Mapped["AnonymousUser"] = relationship(back_populates="history", passive_deletes=True)
    city: Mapped["City"] = relationship(back_populates="history")
