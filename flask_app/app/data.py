from app.common import async_session
from app import models
import sqlalchemy
import datetime


async def count_recent_users() -> int:
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
        return result.scalar_one()


async def top_5_longest_names() -> list:
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
        return list(users.scalars().all())


async def email_domain_proportion(domain: str) -> float:
    '''
    determines the proportion of users with email addresses at the specified domain
    '''
    async with async_session() as session:
        total = await session.execute(
            sqlalchemy.select(
                sqlalchemy.func.count()
            ).select_from(models.User))
        total_count = total.scalar_one()
        if total_count == 0:
            return 0.0
        domain_count = await session.execute(
            sqlalchemy.select(
                sqlalchemy.func.count()
            ).where(models.User.email.like(f'%@{domain}'))
        )
        return domain_count.scalar_one() / total_count

