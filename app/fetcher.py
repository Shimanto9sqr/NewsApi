import httpx, feedparser, asyncio
from datetime import datetime
from dateutil import parser as dparser
from .feeds import FEEDS
from .schemas import HeadlineCreate
from .crud import create_headline

async def fetch_feed(session: httpx.AsyncClient, feed):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; NewsCollector/1.0; +https://example.com)"}
        resp = await session.get(feed["url"], headers=headers, timeout=15.0)
        parsed = feedparser.parse(resp.text)
        items=[]
        for e in parsed.entries:
            published = None
            if "published" in e:
                try:
                    published= dparser.parse(e.published)
                except Exception:
                    published= None
            items.append(
                HeadlineCreate(
                    title=e.get("title", "")[:512],
                    url=e.get("link",""),
                    summary=e.get("summary",""),
                    source= feed["name"],
                    published_at=published,
                )
            )
        return items
    except Exception:
        return[]
    
async def fetch_all_feeds(db_sessionmaker):
    async with httpx.AsyncClient() as client:
        tasks = [fetch_feed(client, f) for f in FEEDS]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_items = [i for r in results if isinstance(r, list) for i in r]
        async with db_sessionmaker() as db:
            for item in all_items:
                await create_headline(db, item)
