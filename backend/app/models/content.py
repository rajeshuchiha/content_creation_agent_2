from app.database import Base
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import func

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    tweet = Column(String)
    blog_post = Column(String)
    reddit_post = Column(String)
    title_embed = Column(Vector(dim=768))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())