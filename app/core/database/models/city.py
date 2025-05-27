from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .search_history import UserCityHistory


class City(Base, IntIdPkMixin):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    search_count: Mapped[int] = mapped_column(default=0, server_default="0", nullable=False)

    # Cвязи
    history: Mapped[list["UserCityHistory"]] = relationship(back_populates="city")
