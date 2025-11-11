from app.database import Base
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import func

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    tweet = Column(String)
    blog_post = Column(String)
    reddit_post = Column(JSON)
    title_embed = Column(Vector(dim=768))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="contents")