from app.database import Base
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class PlatformCredential(Base):
    __tablename__ = "platform_credentials"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # platform_user_id = Column(String, index=True)
    platform = Column(String)
    access_token = Column(String)
    refresh_token = Column(String, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="platforms")
    
    # __table_args__ = (
    #     UniqueConstraint("platform", "platform_user_id", 
    #     name="unique_platform_account")
    # )
    
# platform user id "Not need now."