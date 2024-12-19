import collections.abc
import pytest
import asyncio
import app.common
import flask.testing
import flask


@pytest.fixture()
def testapp() -> collections.abc.Generator:
    asyncio.run(app.common.init_models())
    app.common.app.config.update({
        'TESTING': True,
    })
    yield app.common.app


@pytest.fixture()
def client(testapp: flask.Flask) -> flask.testing.FlaskClient:
    return testapp.test_client()


def test_create_user(
    client: flask.testing.FlaskClient
) -> None:
    r = client.post(
        '/user/create',
        json={
            'username': 'user1',
            'email': 'user1@example.com'
        }
    )
    assert r.status_code == 201


def test_get_user(
    client: flask.testing.FlaskClient
) -> None:
    r = client.get('/user/get?id=1')
    assert r.status_code==200
    assert r.get_json()['username']=='user1'


def test_update_user(
    client: flask.testing.FlaskClient
) -> None:
    r = client.post(
        '/user/update',
        json={
            'id': 1,
            'username': 'user1_new',
            'active_sessions': '2',
            'email': 'user1_new@example.com'
        }
    )
    assert r.status_code == 200


def test_list_all(
    client: flask.testing.FlaskClient
) -> None:
    r = client.get('/user/list-all')
    assert r.status_code == 200
    assert r.get_json()['total_users'] == 1


def test_delete_user(
    client: flask.testing.FlaskClient
) -> None:
    r = client.post(
        '/user/delete',
        json={'id': 1}
    )
    assert r.status_code == 200

