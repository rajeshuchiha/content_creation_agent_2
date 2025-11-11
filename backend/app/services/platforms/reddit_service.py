import os
import httpx
from urllib.parse import urlencode
import secrets
from app.models.platform_credentials import PlatformCredential
from app.schemas.user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime, timedelta

REDIRECT_URI = "http://localhost:8000/api/auth/reddit/callback"

client_id = os.environ.get("reddit_client_ID")
client_secret = os.environ.get("reddit_client_secret")
auth = httpx.BasicAuth(client_id, client_secret)

def get_authorization_url():
    
    state = secrets.token_urlsafe(16)

    params = {
        "client_id": client_id,
        "response_type": "code",
        "state": state,
        "redirect_uri": REDIRECT_URI,
        "duration": "permanent",
        "scope": "read identity submit" #   identity to verify user
    }
  
    authorization_url = f"https://www.reddit.com/api/v1/authorize?{urlencode(params)}"
    return authorization_url, state

    
async def save_credentials(request, db: AsyncSession):
    
    user_id = request.session.get("user_id")
    code = request.query_params.get("code")
    
    headers = {"User-Agent": "web_app/0.1 by Ok_Turnip9330"}
        
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url="https://www.reddit.com/api/v1/access_token", data=data, auth=auth, headers=headers)
        response.raise_for_status()
        credentials = response.json()
        
    async with httpx.AsyncClient() as client:
        response = await client.post(url="https://www.reddit.com/api/v1/access_token", data=data, auth=auth, headers=headers)
        response.raise_for_status()
        credentials = response.json()
        
    expires_at = datetime.now() + timedelta(seconds=credentials["expires_in"])
    db.add(
        PlatformCredential(
            user_id=user_id,
            platform="reddit",
            access_token=credentials["access_token"],
            refresh_token=credentials["refresh_token"],
            expires_at=expires_at
        )
    )
    await db.commit()
    return credentials

# response  = requests.get(url="https://oauth.reddit.com/api/v1/me", headers=headers)

# print(response.json())

# this is the check function (Use it in combined service)
async def check_access_token(db: AsyncSession):
    pass

# Compulsory keys for data. !!! Change "sr" to desired subreddit.
async def postReddit(credentials: PlatformCredential, title = "New Post", text="Place_holder", sr="test"):
    
    # credentials = await db.scalars(
    #     select(PlatformCredential).filter(PlatformCredential.platform == "reddit" & PlatformCredential.user_id==current_user.id)
    # ).first()
    bearer_token = credentials.access_token

    #   **Add this in another function (A check function to check validity)
    # if credentials.get('expires_at') and credentials.expires_at < datetime.now():
        
    
    #     headers = {"User-Agent": "web_app/0.1 by Ok_Turnip9330"}
            
    #     data = {
    #         "grant_type": "refresh_token",
    #         "refresh_token": credentials.refresh_token
    #     }
    #     async with httpx.AsyncClient() as client:
    #         response = await client.post(url="https://www.reddit.com/api/v1/access_token", data=data, auth=auth, headers=headers)
    #         response.raise_for_status()
    #         credentials = response.json()
            
    #     db.add(
    #         PlatformCredential(
    #             user_id=credentials.user_id,
    #             platform="google",
    #             access_token=credentials["access_token"],
    #             refresh_token=credentials["refresh_token"],
    #             expires_at=credentials["expires_in"]
    #         )
    #     )
    #     await db.commit()
    #     bearer_token = credentials["access_token"]        

    
    headers = {"Authorization": f"bearer {bearer_token}", "User-Agent": "ChangeMeClient/0.1 by Ok_Turnip9330"}
    
    if not title:
        print("Reddit post has NULL title.")
        return  

    if not text:
        print("Reddit post has NULL content.")
        return
        
    data = {
            "sr": sr,
            "kind": "self",
            "title": title,
            "text": text
        }    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth.reddit.com/api/submit", 
            headers=headers,
            data=data
        )
        try:
            response.raise_for_status()
            
        except httpx.HTTPStatusError as e:
            print(f"Request failed: {e}")
            
async def check_status(current_user: UserResponse, db: AsyncSession):
    platform = "reddit"
    res = await db.scalars(select(PlatformCredential).where(
        (PlatformCredential.user_id == current_user.id) & 
        (PlatformCredential.platform == platform)
    ))
    results = res.all()    
    
    return {"integrated": len(results) > 0}

async def delete_user(current_user: UserResponse, db: AsyncSession):
    platform = "reddit"
    result = await db.execute(delete(PlatformCredential).where(
        (PlatformCredential.user_id == current_user.id) & 
        (PlatformCredential.platform == platform)
    ))
    await db.commit()
    
    # if result.rowcount == 0:
    #     raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

if __name__ == "__main__":  
# response.status_code()

    postReddit()
