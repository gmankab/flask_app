import sqlalchemy.ext.asyncio
import sqlalchemy
import app.config
import flask


Base = sqlalchemy.orm.declarative_base()
engine = sqlalchemy.ext.asyncio.create_async_engine(
    app.config.db_url,
)


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async_session = sqlalchemy.ext.asyncio.async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=sqlalchemy.ext.asyncio.AsyncSession
)
app = flask.Flask(__name__)

