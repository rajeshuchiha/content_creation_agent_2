from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.content import Content
from app.logger import setup_logger

logger = setup_logger(__name__)

async def get_results(user_id: int, db: AsyncSession):

    try:
        res = await db.scalars(select(Content).where(Content.user_id==user_id))
        results = res.all()
        logger.info("Fetch Successful")
        return results
    except Exception as e:
        logger.error(f"Error: {e}")
        return []