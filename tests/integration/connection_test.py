import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


def test_session(db_session: AsyncSession):
    assert db_session is not None
    assert isinstance(db_session, AsyncSession)


@pytest.mark.asyncio
async def test_database_connection(db_session: AsyncSession):
    query = await db_session.execute(text("SELECT 1;"))
    assert query.scalar() == 1
