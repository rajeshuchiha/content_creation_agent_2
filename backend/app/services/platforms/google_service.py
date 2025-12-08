import os
from app.models.platform_credentials import PlatformCredential
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse
from sqlalchemy import select, delete
import httpx
import secrets
from urllib.parse import urlencode
from app.logger import setup_logger
from app.config import BACKEND_URI
from datetime import timezone, datetime, timedelta
import re

logger = setup_logger(__name__)

SCOPES = ["https://www.googleapis.com/auth/blogger"]
REDIRECT_URI = f"{BACKEND_URI}/api/auth/google/callback"

CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")

# OAuth endpoints
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"

def get_authorization_url():
    
    state = secrets.token_urlsafe(32)  # CSRF protection
    
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",  # Get refresh token
        "prompt": "select_account",
        "state": state,
    }
    
    auth_url = f"{AUTH_URL}?{urlencode(params)}"
    return auth_url, state
    
async def save_credentials(request, db: AsyncSession):
    
    user_id = request.session.get("user_id")
    code = request.query_params.get("code")
        
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
        
    async with httpx.AsyncClient() as client:
        response = await client.post(url=TOKEN_URL, data=data)
        response.raise_for_status()
        credentials = response.json()
    
    #   Ensure timezone-aware
    expires_in = credentials.get("expires_in", 3600)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    
    logger.info(f"expires_at from DB: {expires_at}, tzinfo: {expires_at.tzinfo if expires_at else None}")
    if expires_at and expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    db.add(
        PlatformCredential(
            user_id=user_id,
            platform="google",
            access_token=credentials["access_token"],
            refresh_token=credentials.get("refresh_token"),  # may or may not have refresh_token
            expires_at=expires_at
        )
    )
    await db.commit()
    
    return credentials

async def refresh_access_token(user_creds: PlatformCredential, db: AsyncSession, refresh_token: str):

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()
    
    # Calculate new expiry time
    expires_in = token_data.get("expires_in", 3600)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    
    user_creds.access_token = token_data["access_token"]
    user_creds.expires_at = token_data["expires_at"]
    if token_data["refresh_token"]:
        user_creds.refresh_token = user_creds.refresh_token
        
    await db.commit()
    
    return {
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token"),  # Sometimes Google returns new refresh token
        "expires_at": expires_at,
    }
    
async def get_user_blogs(access_token: str):
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/blogger/v3/users/self/blogs",
            headers=headers
        )
        response.raise_for_status()
        return response.json()

def parse_text(text: str):
    
    # Extract h1 text
    h1_match = re.search(r'<h1>(.*?)</h1>', text, re.IGNORECASE)
    title = h1_match.group(1) if h1_match else "Untitled Post"

    # Remove h1 from content
    content = re.sub(r'<h1>.*?</h1>', '', text, count=1, flags=re.IGNORECASE).strip()

    return title, content
        
async def post_to_blog(access_token: str, blog_id: str, title: str, content: str):
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts",
            headers=headers,
            json=post_data
        )
        response.raise_for_status()
        return response.json()
        
async def postBlog(user_creds: PlatformCredential, db: AsyncSession, text: str):   
   
    expires_at = user_creds.expires_at
    logger.info(f"expires_at from DB: {expires_at}, tzinfo: {expires_at.tzinfo if expires_at else None}")
    
    if expires_at and expires_at.tzinfo is None:
        logger.info("Converting naive datetime to UTC")
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    
    logger.info(f"expires_at after fix: {expires_at}, tzinfo: {expires_at.tzinfo if expires_at else None}")
    
    refresh_token = user_creds.refresh_token
    access_token = user_creds.access_token
    
    now = datetime.now(timezone.utc)
    is_expired = expires_at and now >= expires_at
    
    if is_expired and refresh_token:
        try:
            token_data = refresh_access_token(user_creds, db, refresh_token)
            access_token = token_data["access_token"]
            
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise
        
    #   Posting 
    
    try:
        blogs_data = await get_user_blogs(access_token)
        blogs = blogs_data.get("items", [])
        
        results = []
        for blog in blogs:
            blog_id = blog["id"]
            
            title, content = parse_text(text)
            
            post_result = await post_to_blog(
                access_token, 
                blog_id, 
                title, 
                content
            )
            results.append(post_result.get("url"))
            logger.info(f"Posted to blog: {post_result.get('url')}")
        
        # return {"success": True, "results": results}
    
    except Exception as e:
        logger.error(f"Error posting blog: {e}")
        # return {"success": False, "error": str(e)}
        
       
async def check_status(current_user: UserResponse, db: AsyncSession):
    platform = "google"
    res = await db.scalars(select(PlatformCredential).where(
        (PlatformCredential.user_id == current_user.id) & 
        (PlatformCredential.platform == platform)
    ))
    results = res.all()    
    
    return {"integrated": len(results) > 0}

async def revoke_user_access(current_user: UserResponse, db: AsyncSession, platform):
    stmt = select(PlatformCredential).where(
        (PlatformCredential.user_id == current_user.id) & 
        (PlatformCredential.platform == platform)
    )
    cred = await db.scalar(stmt)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post('https://oauth2.googleapis.com/revoke',
                params={'token': cred.refresh_token},
                headers = {'content-type': 'application/x-www-form-urlencoded'}
            )
            response.raise_for_status()
    except:
        logger.error(f"{platform} revoke error")
        
        
async def delete_user(current_user: UserResponse, db: AsyncSession, platform):

    result = await db.execute(delete(PlatformCredential).where(
        (PlatformCredential.user_id == current_user.id) & 
        (PlatformCredential.platform == platform)
    ))
    await db.commit()
    
    # if result.rowcount == 0:
    #     raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

if __name__ == "__main__":
    text = """
        <h1>MY blog</h1>
    """
    postBlog(text)