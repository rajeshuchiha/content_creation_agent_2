from pydantic import BaseModel
from typing import Annotated, List
from datetime import datetime

class Item(BaseModel):
    id: int
    question: str
    tweet: Annotated[str, "≤15 words, must include hashtags, mentions, emojis"]
    blog_post: Annotated[str, "≥250 words, detailed and informative"]
    reddit_post: Annotated[str, "JSON string with 'title' and 'body'; 'body' supports Markdown"]
    timestamp: datetime
    
    class Config:
        from_attributes = True
    
class ItemsList(BaseModel):
    Items: List[Item]