import asyncio
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from .database import engine, Base, AsyncSessionLocal, get_session
from . import crud, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from .fetcher import fetch_all_feeds
from .feeds import FEEDS

app= FastAPI(title="News Headlines API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    asyncio.create_task(periodic_fetch(300))

async def periodic_fetch(interval:int = 300):
    while True:
        await fetch_all_feeds(AsyncSessionLocal)
        await asyncio.sleep(interval)

@app.get("/")
async def root():
    return {"message":"News Headlines API is running"}

@app.post("/fetch-now")
async def fetch_now():
    asyncio.create_task(fetch_all_feeds(AsyncSessionLocal))
    return{"status":"fetch started"}

@app.get("/headlines/", response_model=List[schemas.HeadlineRead])
async def get_headlines(skip: int=0, limit: int =20, db: AsyncSession= Depends(get_session)):
    return await crud.list_headlines(db, skip, limit)

@app.get("/headlines/{headline_id}", response_model= schemas.HeadlineRead)
async def get_headline(headline_id:int, db:AsyncSession=Depends(get_session)):
    item= await crud.get_headline(db, headline_id)
    if not item:
        raise HTTPException(status_code=404, detail="Headline not found")
    return item

@app.get("/sources")
async def list_source():
    return FEEDS
