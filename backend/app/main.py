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
from sqlalchemy.ext.asyncio import AsyncSession
from google import genai
from google.genai import types
import os
from app.routers import auth
from app.routers.platforms import google, reddit, twitter
from app.database import init_db, get_db
from app.models.content import Content
from app.schemas.user import UserResponse
from app.schemas.content import Item, ItemsList
from app.services.platforms.combined_service import post
from app.services import auth_service
from app.scraper import search, search_and_scrape
from app.services.text_generator import run_document_agent


class Page(BaseModel):
    url: str
    title: str
    text: str
    method: str
    success: bool
    
class PagesList(BaseModel):
    pages: List[Page]
     

llm = init_chat_model('gemini-2.5-flash', model_provider="google_genai")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],    # include frontend(check if changed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("session_secret_key"), # Need to be Static
    https_only=False,      # cookie only sent over HTTPS (Set to True in production)
    max_age=3600,         # seconds, optional
    same_site="lax"
)

app.include_router(auth.router)
app.include_router(google.router)
app.include_router(reddit.router)
app.include_router(twitter.router)

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

@app.get("/api/results/{query}", response_model=ItemsList)
async def content_gen(
    query: str, 
    current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], 
    db: Annotated[AsyncSession, Depends(get_db)], 
    categories: Optional[str]=None      #query parameters(category) must be last
):    
    
    data = await search(query, categories)
    
    titles = []
    total_num_topics = 5
    
    info_list = []
    for res in data["results"]:
        titles.append(res["title"])
        # info_list.append(f'\ntitle: {res["title"]}\ncontent: {res["content"]}')   #   Can use this for more info
    
    questions_text = llm.invoke(
        f'Write {total_num_topics} questions on major topics based on titles: {titles}. '
        'Do NOT number them. Do NOT use "\\n" inside the questions. '
        'Separate each question with a single newline character ("\\n"). '
        'Only output the questions.'
    )

    questions = [q.strip() for q in questions_text.content.split('\n') if q.strip()]
    
    print(questions)
    
    new_items = []
    tone = "curiosity"  #   Can pick a tone on random for each question (write a list to pick random)
    client = genai.Client()
    
    for question in questions:
        
         #   Embedding

        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=question,
            config=types.EmbedContentConfig(output_dimensionality=768)
        )

        [embedding_obj] = result.embeddings
        
        #   Find if question already exists
        existing = await db.scalars(
            select(Content).filter(
                (Content.embedding.cosine_distance(embedding_obj.values) < 0.3)
                & (Content.timestamp > datetime.now() - timedelta(days=2))
            )
        )
        result = existing.first()   # existing.all() for all
        
        if not result:
        
            inputs = [
                f"{question} with a tone of {tone}", 
                "Save it"
            ]
            
            output = await run_in_threadpool(run_document_agent, inputs=inputs, auto=True, categories=categories) #   Second
            
            await asyncio.sleep(8)
            
            #   Add to Content db
            
            result = Content(
                title = question,
                tweet = output.get("tweet", ""),
                blog_post = output.get("blog_post", ""),
                reddit_post = output.get("reddit_post", ""),
                title_embed  = embedding_obj.values,
                timestamp = datetime.now()
            )
        
            db.add(result)
            await db.commit()
            await db.refresh(result)    # Be Cautious! (Don't need to add again)
        
        item = Item.model_validate(result)    
        post(current_user, db, result)    #   Important
        
        # new_items.append({
        #     "question": question,
        #     "tweet": output.get("tweet", ""),
        #     "blog_post": output.get("blog_post", ""),
        #     "reddit_post": output.get("reddit_post", ""),
        #     "timestamp": datetime.now()
        # })
        new_items.append(item)
        
        # the following input must be given to this: 
        # {1. topic -> retrieve 2."write it in a intruiging way and mention every name, date or time exactly " -> update(optional), 3."save it"}
    
    return {"Items": new_items}

@app.get('/health')
async def health_check():
    return {'status': 'ok'}