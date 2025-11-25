from fastapi import FastAPI, Form, Depends
from pydantic import BaseModel
from typing import List, Optional, Annotated, Union
from fastapi.responses import RedirectResponse, HTMLResponse
from langchain.chat_models import init_chat_model
from datetime import datetime, timedelta
import asyncio
from sqlalchemy import select
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from google.genai import types
import os
from app.routers import auth, content
from app.routers.platforms import google, reddit, twitter
from app.database import init_db, get_db
from app.services.platforms.combined_service import post
from app.scraper import search, search_and_scrape
from app.logger import setup_logger
from app.config import allowed_origins

logger = setup_logger(__name__)

class Page(BaseModel):
    url: str
    title: str
    text: str
    method: str
    success: bool
    
class PagesList(BaseModel):
    pages: List[Page]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    await init_db()
    yield
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)
# allow_origins=["http://localhost:3000", "https://content-creation-agent-2.vercel.app/"],    # include frontend(check if changed)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("session_secret_key"), # Need to be Static
    session_cookie="session",
    https_only=True,      # cookie only sent over HTTPS (Set to True in production)
    max_age=3600,         # seconds, optional
    same_site="lax"
)

app.include_router(auth.router)
app.include_router(google.router)
app.include_router(reddit.router)
app.include_router(twitter.router)
app.include_router(content.router)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <form action="/api" method="post">
        <input type="text" name="query" placeholder="Enter Here...">
        <label><input type="checkbox" name="news" value="news"> news</label>
        <button type="submit" value="Scrape">Generate</button>
    </form>
    """

@app.post("/api")
async def api(query: str = Form(...), news: str = Form(None)):
    
    target_url = f'/api/results/{query}'
    
    if news:
        target_url = f"/api/results/{query}?categories=news"
    
    return RedirectResponse(target_url, status_code=303)

@app.get("/api/search/{query}")
async def get_search_results(query: str, categories: Optional[str]=None):
    return await search(query, categories)

@app.get("/api/scrape/{query}", response_model=PagesList)
async def get_scrape_data(query: str, categories: Optional[str]=None):
    
    results = await search_and_scrape(query, categories, maxURL=5)
    
    return {"pages": results}

@app.get('/health')
async def health_check():
    return {'status': 'ok'}