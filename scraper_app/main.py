from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List, Optional, Annotated, Union
import httpx
from scraper import Scraper
from fastapi.responses import RedirectResponse, HTMLResponse

class Page(BaseModel):
    url: str
    title: str
    text: str
    method: str
    success: bool
    
class PagesList(BaseModel):
    pages: List[Page]

async def search(query, categories):
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            # res = await client.get(f"http://search_engine:8080/search?q={query}&categories={categories}&format=json")
            res = await client.get("http://search_engine:8080/search", 
                                    params={
                                        "q": query,
                                        "categories": categories,
                                        "format": "json"
                                    })
            return res.json()
    
    except Exception as e: 
        print(f"Search failed: {e}")
        return {"results": []}
    
async def search_and_scrape(query, categories, maxURL=10):
    
    data = await search(query, categories)
    urls = [page["url"] for page in data["results"] if page.get("url")][:maxURL]
    
    scraper = Scraper()
    results = await scraper.scrape_multiple(urls=urls)  
      
    return results

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