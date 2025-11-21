from fastapi import APIRouter, Depends
from typing import Optional, Annotated
from langchain.chat_models import init_chat_model
# from datetime import datetime, timedelta
# import json
# import asyncio
# from sqlalchemy import select
# from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
# from google import genai
# from google.genai import types
from app.database import get_db
# from app.models.content import Content
from app.schemas.user import UserResponse
# from app.schemas.content import Item, ItemsList
# from app.services.platforms.combined_service import post
from app.services import auth_service
# from app.scraper import search
# from app.services.text_generator import run_document_agent
# from app.celery_app import celery
from app.tasks import search_task, generate_questions, process_llm, content_post
from celery import chain
from app.celery_app import celery
from app.logger import setup_logger

logger = setup_logger(__name__)


router = APIRouter(prefix='/api/results', tags=["content"])

@router.post("/{query}")
async def content_gen(
    query: str, 
    current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], 
    db: Annotated[AsyncSession, Depends(get_db)], 
    categories: Optional[str]=None      #query parameters(category) must be last
):

    try:
        
        workflow = chain(
            search_task.s(query, categories),
            generate_questions.s(),
            process_llm.s(current_user_id=current_user.id),
            content_post.s(current_user_id=current_user.id)
        )
        
        result = workflow.apply_async()
        
        return {
            "status": result.status,
            "task_id": result.id
        }

    except Exception as e:
        logger.exception(f"Task Error: {e}")
        return {
            "error": str(e),
            "status": "failed"
        }

@router.get("/{task_id}")
def get_status(task_id: str):
    
    result = celery.AsyncResult(task_id)
    
    return {
        "task_id": task_id,
        "status": result.status,    # PENDING / STARTED / SUCCESS / FAILURE
        "result": result.result     # None until finished
    }
    
# llm = init_chat_model('gemini-2.5-flash', model_provider="google_genai")

# @router.get("/{query}", response_model=ItemsList)
# async def content_gen(
#     query: str, 
#     current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], 
#     db: Annotated[AsyncSession, Depends(get_db)], 
#     categories: Optional[str]=None      #query parameters(category) must be last
# ):    
    
#     data = await search(query, categories)
    
#     titles = []
#     total_num_topics = 2
    
#     # info_list = []
#     for res in data["results"]:
#         titles.append(res["title"])
#         # info_list.append(f'\ntitle: {res["title"]}\ncontent: {res["content"]}')   #   Can use this for more info
    
#     questions_text = llm.invoke(
#         f'Write {total_num_topics} questions on major topics based on titles: {titles}. '
#         'Do NOT number them. Do NOT use "\\n" inside the questions. '
#         'Separate each question with a single newline character ("\\n"). '
#         'Only output the questions.'
#     )

#     questions = [q.strip() for q in questions_text.content.split('\n') if q.strip()]
    
#     print(questions)
    
    
#     # tone = ["happy", "curiosity", "sad", "anger"] #   Can pick a tone on random for each question (write a list to pick random)
#     client = genai.Client()
    
#     results = []
#     new_items = []
    
#     for question in questions:
        
#          #   Embedding

#         res = client.models.embed_content(
#             model="gemini-embedding-001",
#             contents=question,
#             config=types.EmbedContentConfig(output_dimensionality=768)
#         )

#         [embedding_obj] = res.embeddings
        
#         #   Find if question already exists
#         existing = await db.scalars(
#             select(Content).filter(
#                 (Content.title_embed.cosine_distance(embedding_obj.values) < 0.3)   #   0.3 strict can be 0.35
#                 & (Content.timestamp > datetime.now() - timedelta(days=2))
#                 & (Content.tweet != "")
#                 & (Content.blog_post != "")
#                 & (Content.reddit_post != None)
#             )
#         )

#         result = existing.first()   # existing.all() for all
        
#         # result = None   # comment out later
        
#         if not result:
        
#             inputs = [
#                 f"{question}", 
#                 "Save it"
#             ]
            
#             output = await run_in_threadpool(run_document_agent, current_user, db, inputs=inputs, auto=True, categories=categories) #   Second
            
#             await asyncio.sleep(8)
            
#             #   Add to Content db
#             raw = output.get("reddit_post", "{}")
#             try:
#                 reddit_data = json.loads(raw)
#             except json.JSONDecodeError:
#                 reddit_data = {}  
            
#             result = Content(
#                 user_id = current_user.id,
#                 title = question,
#                 tweet = output.get("tweet", ""),
#                 blog_post = output.get("blog_post", ""),
#                 reddit_post = reddit_data,
#                 title_embed  = embedding_obj.values,
#                 timestamp = datetime.now()
#             )
        
#             db.add(result)
#             await db.flush()
#         results.append(result)
        
#     #   Batch Commit
#     try:
#         await db.commit()
#     except Exception as e:
#         await db.rollback()
#         print("DB COMMIT FAILED:", e)
#         raise
            
#     for result in results:
        
#         try:
#             await asyncio.wait_for(
#                 post(current_user, db, result),
#                 timeout=25  # Prevent infinite hang
#             )
#         except Exception as e:
#             print(f"POST FAILED for {result.title}: {e}")

#         new_items.append(Item.model_validate(result))


#         # the following input must be given to this: 
#         # {1. topic -> retrieve 2."write it in a intruiging way and mention every name, date or time exactly " -> update(optional), 3."save it"}
    
#     print(new_items)
    
#     return {"Items": new_items}