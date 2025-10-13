from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List, Optional, Annotated, Union
from fastapi.responses import RedirectResponse, HTMLResponse
from langchain.chat_models import init_chat_model
from datetime import datetime
import asyncio
from fastapi.concurrency import run_in_threadpool
from scraper import search, search_and_scrape
from generation.text_generator import run_document_agent

class Page(BaseModel):
    url: str
    title: str
    text: str
    method: str
    success: bool
    
class PagesList(BaseModel):
    pages: List[Page]
    
class Item(BaseModel):
    question: str
    tweet: Annotated[str, "≤15 words, must include hashtags, mentions, emojis"]
    blog_post: Annotated[str, "≥250 words, detailed and informative"]
    reddit_post: Annotated[str, "JSON string with 'title' and 'body'; 'body' supports Markdown"]
    timestamp: datetime
    
class ItemsList(BaseModel):
    Items: List[Item]
     

llm = init_chat_model('gemini-2.5-flash', model_provider="google_genai")

app = FastAPI()

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
async def content_gen(query: str, categories: Optional[str]=None):
    
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
    for question in questions:
        inputs = [
            f"{question} with a tone of {tone}", 
            "Save it"
        ]
        
        output = await run_in_threadpool(run_document_agent, inputs=inputs, auto=True, categories=categories) #   Second
        
        await asyncio.sleep(8)
        
        #   output is giving empty tweet, blog, reddit. Check WHY??
        
        new_items.append({
            "question": question,
            "tweet": output.get("tweet", ""),
            "blog_post": output.get("blog_post", ""),
            "reddit_post": output.get("reddit_post", ""),
            "timestamp": datetime.now()
        })
        # the following input must be given to this: 
        # {1. topic -> retrieve 2."write it in a intruiging way and mention every name, date or time exactly " -> update(optional), 3."save it"}
    
    return {"Items": new_items}