from app.common import app, async_session
from app import models
import sqlalchemy
import datetime
import flask
import typing


@app.get('/data/count-recent')
async def data_count_recent() -> tuple[dict[str, int], int]:
    '''
    counts the number of users registered in the last 7 days
    '''
    cutoff = int(
        (
            datetime.datetime.now(
                datetime.timezone.utc
            ) - datetime.timedelta(days=7)
        ).timestamp()
    )
    async with async_session() as session:
        result = await session.execute(
            sqlalchemy.select(sqlalchemy.func.count()).where(models.User.registration_date >= cutoff)
        )
        count = result.scalar_one()
    return {'count': count}, 200


@app.get('/data/top-longest')
async def data_top_longest() -> tuple[dict[str, typing.List[str]], int]:
    '''
    returns the top 5 users with the longest usernames
    '''
    async with async_session() as session:
        users = await session.execute(
            sqlalchemy.select(
                models.User
            ).order_by(
                sqlalchemy.func.length(
                    models.User.username
                ).desc()
            ).limit(5)
        )
        users_list = users.scalars().all()
    return {'users': [u.username for u in users_list]}, 200


@app.get('/data/proportion')
async def data_proportion() -> tuple[dict[str, typing.Any], int]:
    '''
    determines the proportion of users with email addresses at the specified domain
    '''
    domain = flask.request.args.get('domain')
    assert domain
    async with async_session() as session:
        total = await session.execute(
            sqlalchemy.select(
                sqlalchemy.func.count()
            ).select_from(models.User)
        )
        total_count = total.scalar_one()
        if total_count == 0:
            proportion = 0.0
        else:
            domain_count = await session.execute(
                sqlalchemy.select(
                    sqlalchemy.func.count()
                ).where(models.User.email.like(f'%@{domain}'))
            )
            domain_count_val = domain_count.scalar_one()
            proportion = domain_count_val / total_count
    return {'domain': domain, 'proportion': proportion}, 200

