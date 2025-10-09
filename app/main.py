from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List, Optional, Annotated, Union
from app.scraper import search, search_and_scrape
from fastapi.responses import RedirectResponse, HTMLResponse


class Page(BaseModel):
    url: str
    title: str
    text: str
    method: str
    success: bool
    
class PagesList(BaseModel):
    pages: List[Page]



app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <form action="/api" method="post">
        <input type="text" name="query" placeholder="Enter Here...">
        <label><input type="checkbox" name="news" value="news"> news</label>
        <button type="submit" value="Scrape">Search</button>
    </form>
    """

@app.post("/api")
async def api(query: str = Form(...), news: str = Form(None)):
    
    target_url = f'/api/scrape/{query}'
    
    if news:
        target_url = f"/api/scrape/{query}?categories=news"
    
    return RedirectResponse(target_url, status_code=303)

@app.get("/api/search/{query}")
async def get_search_results(query: str, categories: Optional[str]=None):
    return await search(query, categories)

@app.get("/api/scrape/{query}", response_model=PagesList)
async def get_scrape_data(query: str, categories: Optional[str]=None):
    
    results = await search_and_scrape(query, categories, maxURL=10)
    
    return {"pages": results}

@app.get("/api/results/{query}")
async def content_gen(query: str, categories: Optional[str]=None):
    
    data = search(query, categories)
    results = await search_and_scrape(query, categories, data, maxURL=10)
    
    return {"pages": results}