from app.common import app, async_session
from app import models, schemas, predict
import sqlalchemy
import traceback
import datetime
import typing
import flask


@app.post('/user/create')
async def user_create() -> tuple[str, int]:
    '''create a new user'''
    data = schemas.UserCreate(**flask.request.get_json())
    async with async_session() as session:
        user = models.User(
            username=data.username,
            email=data.email,
            active_sessions=1,
            registration_date=int(
                datetime.datetime.now(
                    datetime.timezone.utc
                ).timestamp()
            )
        )
        session.add(user)
        await session.commit()
    return 'created', 201


@app.get('/user/get')
async def user_get() -> tuple[dict[str, typing.Any], int]:
    '''get a user by id'''
    data = schemas.UserGet(
        id = int(flask.request.args['id'])
    )
    async with async_session() as session:
        user: models.User = await session.get(models.User, data.id)
    assert user
    predict_activity = await predict.predict_activity(user.id)
    return schemas.User(
        id=user.id,
        username=user.username,
        email=user.email,
        active_sessions=user.active_sessions,
        registration_date=user.registration_date,
        predict_activity=predict_activity,
    ).model_dump(), 200


@app.post('/user/update')
async def user_update() -> tuple[str, int]:
    '''update a user'''
    data = schemas.UserUpdate(**flask.request.get_json())
    async with async_session() as session:
        user: models.User = await session.get(models.User, data.id)
        assert user
        if data.username:
            user.username = data.username
        if data.email:
            user.email = data.email
        if data.active_sessions:
            user.active_sessions = data.active_sessions
        await session.commit()
    return 'updated', 200


@app.post('/user/delete')
async def user_delete() -> tuple[str, int]:
    '''delete a user'''
    data = schemas.UserDelete(**flask.request.get_json())
    async with async_session() as session:
        user: models.User = await session.get(models.User, data.id)
        assert user
        await session.delete(user)
        await session.commit()
    return 'deleted', 200


@app.get('/user/list-all')
async def user_list_all() -> dict[str, typing.Any]:
    '''list all users'''
    users_per_page = 10
    data = schemas.UserListAll(
        page = int(flask.request.args.get('page', 1))
    )
    assert data.page >= 1
    async with async_session() as session:
        total_users_result = await session.execute(
            sqlalchemy.select(sqlalchemy.func.count(models.User.id))
        )
        total_users = total_users_result.scalar_one()
        total_pages = (total_users // users_per_page) + 1
        print()
        if data.page > total_pages and total_users != 0:
            raise ValueError(f'{data.page} page requested, but only {total_pages} pages exist')
        offset = (data.page - 1) * users_per_page
        users_query = sqlalchemy.select(
            models.User
        ).order_by(
            models.User.id
        ).offset(
            offset
        ).limit(users_per_page)
        users_result = await session.execute(users_query)
        users_data: list[dict] = []
        for user in users_result.scalars().all():
            predict_activity = await predict.predict_activity(user.id)
            users_data.append(
                schemas.User(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    active_sessions=user.active_sessions,
                    registration_date=user.registration_date,
                    predict_activity=predict_activity,
                ).model_dump()
            )
    return schemas.UserListAllResponse(
        users=users_data,
        total_pages=total_pages,
        current_page=data.page,
        total_users=total_users
    ).model_dump()


@app.errorhandler(Exception)
def handle_bad_request(e: Exception) -> tuple[str, int]:
    traceback.print_exception(e)
    return f'{type(e)}: {e}', 400

