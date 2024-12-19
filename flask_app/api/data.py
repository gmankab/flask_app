from app.common import app, async_session
from app import models
import sqlalchemy
import datetime
import flask
import typing


@app.get('/data/count-recent')
async def data_count_recent() -> tuple[dict[str, int], int]:
    '''
    count recently registered users in the last 7 days

    this endpoint returns the number of users who registered within the last 7 days
    ---
    responses:
      200:
        schema:
          type: object
          properties:
            count:
              type: integer
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
    retrieve the top 5 users with the longest usernames

    this endpoint queries the database and returns the top 5 users ordered by the length of their username in descending order
    ---
    responses:
      200:
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                type: string
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
    determine the proportion of users with email addresses at a specified domain

    this endpoint calculates the fraction of users who have email addresses ending with the given domain
    ---
    parameters:
      - name: domain
        in: query
        required: true
        type: string
    responses:
      200:
        schema:
          type: object
          properties:
            domain:
              type: string
            proportion:
              type: number
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

