from app.common import async_session
from app import models
import collections.abc
import flask.testing
import flask
import app.common
import datetime
import asyncio
import pytest


@pytest.fixture()
def testapp() -> collections.abc.Generator:
    asyncio.run(app.common.init_models())
    app.common.app.config.update({'TESTING': True})
    yield app.common.app


@pytest.fixture()
def client(testapp: flask.Flask) -> flask.testing.FlaskClient:
    return testapp.test_client()


def test_count_recent(client: flask.testing.FlaskClient) -> None:
    async def prepare() -> None:
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
    asyncio.run(prepare())
    r = client.get('/data/count-recent')
    assert r.status_code == 200
    data = r.get_json()
    assert data['count'] == 2


def test_top_longest(client: flask.testing.FlaskClient) -> None:
    async def prepare() -> None:
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
    asyncio.run(prepare())
    r = client.get('/data/top-longest')
    assert r.status_code == 200
    data = r.get_json()
    assert data["users"] == [
        '123456',
        '12345',
        '1234',
        '123',
        '12',
    ]


def test_data_proportion(client: flask.testing.FlaskClient) -> None:
    async def prepare() -> None:
        async with async_session() as session:
            await session.execute(models.User.__table__.delete())
            await session.commit()
            now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            session.add(models.User(username='user1', email='user1@gmail.com', registration_date=now))
            session.add(models.User(username='user2', email='user2@gmail.com', registration_date=now))
            session.add(models.User(username='user3', email='user3@yahoo.com', registration_date=now))
            await session.commit()
    asyncio.run(prepare())
    r = client.get('/data/proportion?domain=gmail.com')
    assert r.status_code == 200
    data = r.get_json()
    assert data['proportion'] == 2/3

    r = client.get('/data/proportion?domain=yahoo.com')
    assert r.status_code == 200
    data = r.get_json()
    assert data['proportion'] == 1/3

    r = client.get('/data/proportion?domain=example.com')
    assert r.status_code == 200
    data = r.get_json()
    assert data['proportion'] == 0

