from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .models import Headline
from .schemas import HeadlineCreate

async def create_headline(db: AsyncSession, item: HeadlineCreate):
    obj= Headline(
        title=item.title.strip(),
        url=item.url.strip(),
        summary=(item.summary or "").strip(),
        source=(item.source or "").strip(),
        published_at=item.published_at,
    )
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except IntegrityError:
        await db.rollback()
        return None
    
async def list_headlines(db: AsyncSession, skip: int=0, limit: int =50):
    stmt= select(Headline).order_by(Headline.fetched_at.desc()).offset(skip).limit(limit)
    result= await db.execute(stmt)
    return result.scalars().all()

async def get_headline(db: AsyncSession, headline_id: int):
    return await db.get(Headline, headline_id)