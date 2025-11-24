from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text
from app.config import DB_URL

engine = create_async_engine(DB_URL, echo=True)

Base = declarative_base()


# Base.metadata.create_all(engine)
async_session_maker = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False
)

async def init_db():
    """Call this once at application startup"""
    async with engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))

async def get_db():   
    async with async_session_maker() as session:
        yield session