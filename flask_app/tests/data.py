import app.common
import app.data
import pytest
import datetime
import pytest_asyncio
from app.common import async_session
from app import models


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    await app.common.init_models()


@pytest.mark.asyncio
async def test_count_recent_users():
    async with async_session() as session:
        await session.execute(models.User.__table__.delete())
        await session.commit()
        now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        old = now - (8 * 24 * 3600)
        session.add_all([
            models.User(username='recent1', email='r1@example.com', registration_date=now),
            models.User(username='recent2', email='r2@example.com', registration_date=now),
            models.User(username='old1', email='o1@example.com', registration_date=old),
        ])
        await session.commit()
        assert await app.data.count_recent_users() == 2


@pytest.mark.asyncio
async def test_top_5_longest_names():
    async with async_session() as session:
        await session.execute(models.User.__table__.delete())
        await session.commit()
        now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        names = [
            '1',
            '12',
            '123',
            '1234',
            '12345',
            '123456',
        ]
        for n in names:
            session.add(
                models.User(username=n, email=f'{n}@example.com', registration_date=now)
            )
        await session.commit()
        longest = await app.data.top_5_longest_names()
        assert [u.username for u in longest] == [
            '123456',
            '12345',
            '1234',
            '123',
            '12',
        ]


@pytest.mark.asyncio
async def test_email_domain_proportion():
    async with async_session() as session:
        await session.execute(models.User.__table__.delete())
        await session.commit()
        now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        session.add(models.User(username='user1', email='user1@gmail.com', registration_date=now))
        session.add(models.User(username='user2', email='user2@gmail.com', registration_date=now))
        session.add(models.User(username='user3', email='user3@yahoo.com', registration_date=now))
        await session.commit()
        assert await app.data.email_domain_proportion('gmail.com') == 2 / 3
        assert await app.data.email_domain_proportion('yahoo.com') == 1 / 3
        assert await app.data.email_domain_proportion('example.com') == 0

