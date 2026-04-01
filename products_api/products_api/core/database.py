from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from products_api.core.settings import Settings

engine = create_async_engine(Settings().database_url, echo=True)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
