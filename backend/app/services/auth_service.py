from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime
from ..models.user import User
from ..schemas.user import UserModel, UserInDB, Token

#   openssl rand -hex 32  (command)
SECRET_KEY = "4ed5fafed291cca71e7b0b859d10b60285e1e03ee404198ebf389294242bd532"  # use env var in prod
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    

# helper functions
def get_hashed_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def get_user(db, username: str):
    
    user = db.query(User).filter(User.username == username).first()
    
    if user:
        # return UserInDB(**user)     # **user, giving values of dict as arguments (if user is dict)    
        return UserInDB.model_validate(user)
    
def authenticate_user(db, username, password):
    
    user = get_user(db, username)
    
    # if not user:
    #     user = db.query(User).filter(User.email == username).first()    #      Verify by email too
    if not user:
        return False

    if not verify_password(password, user["hashed_password"]):
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
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY ,algorithms=ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = Token(username=username)   # check why this is used
    except:
        raise credentials_exception
    
    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],   # UserInDB can be passed to User (inheritance, hash_pass will be ignored)
):
    if current_user.disabled:
        raise HTTPException(
            status_code=400, detail='Inactive User')     
    return current_user

def create_user(db, user):
    
    existing = db.query(User).filter(User.username == user.username).first()

    if existing:
        raise HTTPException(status_code=400, detail="username already exists!")
    
    db_user = {
        "username": user["username"],
        "email": user["username"],
        "password": get_hashed_password(user["password"])
    }
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)     #   Adjusts db_user to UserResponse
    
    return db_user
    

        
