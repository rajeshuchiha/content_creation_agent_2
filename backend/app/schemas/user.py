from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True

        
#   Still pending... (learn first)

class Token(BaseModel):
    access_token: str
    token_type: str

# class UserModel(BaseModel):
#     username: str
#     email: str | None = None
#     # disabled: bool | None = None
#     is_active: bool | None = None
#     class Config:
#         from_attributes = True      #   for changing from orm (sqlalchemy)
    
class UserInDB(UserResponse):
    hashed_password: str