from pydantic import BaseModel, ConfigDict
from typing import Annotated, List
from datetime import datetime

class RedditContent(BaseModel):
    title: str
    body: str

class Item(BaseModel):
    id: int
    title: str
    tweet: Annotated[str, "≤15 words, must include hashtags, mentions, emojis"]
    blog_post: Annotated[str, "≥250 words, detailed and informative"]
    reddit_post: Annotated[RedditContent | None, "JSON with 'title' and 'body'; 'body' supports Markdown"] = None
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class ItemsList(BaseModel):
    items: List[Item]
    
    # model_config = ConfigDict(from_attributes=True)