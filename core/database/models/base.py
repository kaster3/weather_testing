from sqlalchemy import UniqueConstraint, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from core import settings
from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    # переопределяем базовою metadata потому что у алхимии есть проблема с constraints из-за
    # которых alembic генерирует миграции с их добавлением только на индексы, а на остальные
    # без naming conventions нужно будет вводить вручную
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    # автоматическая генерация имени таблицы на основе название класса (CamelCase -> snake_case)
    # декоратор показывает что нужно сделать это в момент объявление класса, а не создания экземпляра
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    # foo: Mapped[int]
    # bar: Mapped[int]
    #
    # __table_args__ = (
    #     UniqueConstraint("foo", "bar"),
    # )