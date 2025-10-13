from ..database import Base
from sqlalchemy import  Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)      # index=True -> fast lookup by 
    hashed_password = Column(String, nullable=False)

    platforms = relationship("PlatformCredential", back_populates="user")