from langchain.chat_models import init_chat_model
from datetime import datetime, timedelta
import json
import asyncio
from sqlalchemy import select
from fastapi.concurrency import run_in_threadpool
from google import genai
from google.genai import types
from celery import shared_task
from app.database import async_session_maker
from app.models.content import Content
from app.models.user import User
from app.schemas.content import Item
from app.services.platforms.combined_service import post
from app.scraper import search
from app.services.text_generator import run_document_agent
from app.celery_app import celery
from app.logger import setup_logger

logger = setup_logger(__name__)

def run_async(coro):
    """
    Safely run async code inside synchronous Celery tasks.
    Reuses the same event loop throughout the worker lifetime.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # No loop exists → create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Loop might exist but be closed
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Avoid "event loop already running" error (rare case)
    if loop.is_running():
        raise RuntimeError(
            "run_async() was called inside a running event loop. "
            "Use 'await coro' instead."
        )

    return loop.run_until_complete(coro)


llm = init_chat_model('gemini-2.5-flash', model_provider="google_genai")

 
async def process_questions(questions, categories, current_user_id):   
    
    async with async_session_maker() as session:
        
        res = await session.scalars(select(User).filter(User.id == current_user_id))
        current_user = res.first()
        
        # tone = ["happy", "curiosity", "sad", "anger"] #   Can pick a tone on random for each question (write a list to pick random)
        client = genai.Client()
        results = []
        
        for question in questions:
            
            #   Embedding
            res = client.models.embed_content(
                model="gemini-embedding-001",
                contents=question,
                config=types.EmbedContentConfig(output_dimensionality=768)
            )

            [embedding_obj] = res.embeddings
            
            #   Find if question already exists
            existing = await session.scalars(
                select(Content).filter(
                    (Content.title_embed.cosine_distance(embedding_obj.values) < 0.3)   #   0.3 strict can be 0.35
                    & (Content.timestamp > datetime.now() - timedelta(days=2))
                    & (Content.tweet != "")
                    & (Content.blog_post != "")
                    & (Content.reddit_post != None)
                )
            )

            result = existing.first()   # existing.all() for all
            
            # result = None   # comment out later
            
            if not result:
            
                inputs = [
                    f"{question}", 
                    "Save it"
                ]
                
                output = await run_in_threadpool(run_document_agent, current_user, session, inputs=inputs, auto=True, categories=categories) #   Second
                logger.info(f"\nOutput of text_generator\n: {output}")
                await asyncio.sleep(8)
                
                #   Add to Content db
                raw = output.get("reddit_post", {"title": "", "body": ""})
                try:
                    reddit_data = json.loads(raw)
                except json.JSONDecodeError:
                    reddit_data = {"title": "", "body": ""}  
                
                result = Content(
                    user_id = current_user.id,
                    title = question,
                    tweet = output.get("tweet", ""),
                    blog_post = output.get("blog_post", ""),
                    reddit_post = reddit_data,
                    title_embed  = embedding_obj.values,
                    timestamp = datetime.now()
                )
            
                session.add(result)
                await session.flush()
            results.append(result)
            
        #   Batch Commit
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.exception(f"SESSION COMMIT FAILED: {e}")
            raise
        
        return results        

async def post_content(result_ids, current_user_id):
    
    async with async_session_maker() as session:
        
        res = await session.scalars(select(User).filter(User.id == current_user_id))
        current_user = res.first()
    
        new_items = []
        
        for id in result_ids:
                
            try:
                rows = await session.scalars(select(Content).filter(Content.id == id))
                result = rows.first()
                item = Item.model_validate(result)
                new_items.append(item)
                await asyncio.wait_for(
                    post(current_user, session, item),
                    timeout=25  # Prevent infinite hang
                )
            except Exception as e:
                logger.warning(f"POST FAILED for {result.title}: {e}")

        print(new_items)
    
    # return {"items": new_items}

# @celery.task(name='app.tasks.search_task')
@celery.task(bind=False)
def search_task(query, categories):
    
    data = run_async(search(query, categories))
    
    if not data["results"]:
        logger.error("Null results from search task")
        return {
            "error": True
        }
    
    titles = [res["title"] for res in data["results"] if res and res.get("title")]

    logger.info(f"search task, produced results: {titles}")
    return {
        "query": query,
        "titles": titles,
        "categories": categories,
        "data": data
    }

# @celery.task(name='app.tasks.generate_questions')
@celery.task(bind=False)
def generate_questions(search_data: dict):
    
    if search_data.get("error"):
        return search_data
    
    titles = search_data["titles"]
    total_num_topics = 2
    
    questions_text = llm.invoke(
        f'Write {total_num_topics} questions on major topics based on titles: {titles}. '
        'Do NOT number them. Do NOT use "\\n" inside the questions. '
        'Separate each question with a single newline character ("\\n"). '
        'Only output the questions.'
    )

    questions = [q.strip() for q in questions_text.content.split('\n') if q.strip()]
    
    if not questions:
        logger.error("Empty questions from 'generate_questions' task")
        return {
            "error": True
        }
    
    logger.info(f"generate questions task produced following questions. {questions}")
    
    return {
        **search_data,
        "questions": questions
    }
    
# @celery.task(name='app.tasks.process_llm')
@celery.task(bind=False)
def process_llm(data: dict, current_user_id):
    
    if data.get("error"):
        return data
       
    questions = data["questions"]
    categories = data["categories"]
    
    results = run_async(process_questions(questions, categories, current_user_id)) 
    
    result_ids = [result.id for result in results]
    
    logger.info("process_llm successfully executed")
    
    return {
        "questions": questions,
        "result_ids": result_ids,
        "total_processed": len(results)
    }
    
    
# @celery.task(name='app.tasks.content_post')
@celery.task(bind=False)
def content_post(data: dict, current_user_id):
    
    if data.get("error"):
        return {
            "status": "failed"
        }

    result_ids = data["result_ids"]
    
    run_async(post_content(result_ids, current_user_id))
    
    return{
        "status": "completed"
    }

