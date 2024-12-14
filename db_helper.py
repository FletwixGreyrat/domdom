from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class DataBaseHelper():
    def __init__(self, url, echo):
        self.engine = create_async_engine(url=url, echo=echo)

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    
    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session

            await session.close()


db_helper = DataBaseHelper(url=settings.url, echo=settings.echo)
