from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.context import CryptContext
from pwdlib import PasswordHash
import jwt
from datetime import timedelta, datetime
from app.models.user import User
from app.schemas.user import UserInDB
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

#   openssl rand -hex 32  (command)
SECRET_KEY = "4ed5fafed291cca71e7b0b859d10b60285e1e03ee404198ebf389294242bd532"  # use env var in prod
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")     #   Check the prefix in auth.py
    

# helper functions
def get_hashed_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed: str):
    return password_hash.verify(password, hashed)


async def get_user(db, username: str):
    
    result = await db.execute(select(User).where(User.username == username))     #   For async db.
    user = result.scalars().first()
    
    if user:
        # return UserInDB(**user)     # **user, giving values of dict as arguments (if user is dict)    
        return UserInDB.model_validate(user)
    
async def authenticate_user(db, username, password):
    user = await get_user(db, username)
    # if not user:
    #     user = db.query(User).filter(User.email == username).first()    #      Verify by email too
    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False
    
    return user

#   Create jwt access token 
def create_access_token(data: dict, expires_delta: timedelta|None = None):
    to_encode = data.copy()
    if expires_delta:
        expiry = datetime.now() + expires_delta
    else:
        expiry = datetime.now() + timedelta(minutes=15)
        
    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# token -> user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        # token_data = Token(access_token=username)   # check why this is used
    except:
        raise credentials_exception
    
    user = await get_user(db, username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],   # UserInDB can be passed to User (inheritance, hash_pass will be ignored)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=400, detail='Inactive User')     
    return current_user

async def create_user(db, user):
    
    result = await db.execute(select(User).where(User.username == user.username))     #   For async db.
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="username already exists!")
    
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_hashed_password(user.password)
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user
  

        
