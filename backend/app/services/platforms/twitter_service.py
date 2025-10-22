import os
import httpx
from urllib.parse import urlencode
import secrets
from app.models.platform_credentials import PlatformCredential
from app.schemas.user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from requests_oauthlib import OAuth1

REDIRECT_URI = "http://localhost:8000/auth/twitter/callback"

oauth_consumer_key = os.environ.get("twitter_API_key")
oauth_consumer_key_secret = os.environ.get("twitter_API_key_secret")

async def get_authorization_url():
    
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.x.com/oauth/request_token", 
            params={
                "oauth_callback": REDIRECT_URI,     #   encoded url (is already encoded by urlencode so, no need of quote())
                "oauth_consumer_key": oauth_consumer_key
            }
        )
        
        data = res.json()
        
    state = secrets.token_urlsafe(16)

    params = {
        "oauth_token": data.get("oauth_token")
    }
  
    authorization_url = f"https://api.x.com/oauth/authorize?{urlencode(params)}"
    return authorization_url, state

    
async def save_credentials(request, current_user: UserResponse, db: AsyncSession):
    
    oauth_token = request.query_params.get('oauth_token')
    oauth_verifier = request.query_params.get('oauth_verifier')
    
    auth = {
        "oauth_consumer_key": oauth_consumer_key,
        "oauth_token": oauth_token,
        "oauth_verfier": oauth_verifier
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url="https://api.x.com/oauth/access_token", auth=auth) 
        response.raise_for_status()
        credentials = response.json()
        
    db.add(
        PlatformCredential(
            user_id=current_user.id,
            platform="twitter",
            access_token=credentials["oauth_token"],
            refresh_token=credentials["oauth_token_secret"],    # Not refresh_token **Remember**
            expires_at=None
        )
    )
    await db.commit()
    return credentials


async def postTweet(credentials: PlatformCredential, tweet):

    
    access_token = credentials.access_token
    access_token_secret = credentials.refresh_token
    
    if not tweet:
        print("Reddit post has NULL tweet.")
        return  

        
    auth = OAuth1(
        oauth_consumer_key,
        oauth_consumer_key_secret,
        access_token,
        access_token_secret
    )

    async with httpx.AsyncClient() as client:
        response = client.post(
            "https://api.x.com/statuses/update.json", 
            auth=auth,
            data={"status": tweet}
        )
        try:
            response.raise_for_status()
            
        except httpx.HTTPStatusError as e:
            print(f"Request failed: {e}")
            
            
async def check_status(current_user: UserResponse, db: AsyncSession):
    platform = "twitter"
    res = await db.scalars(select(PlatformCredential).where(
        (PlatformCredential.user_id == current_user.id) & 
        (PlatformCredential.platform == platform)
    ))
    results = res.all()    
    
    return {"integrated": results is not None}

async def delete_user(current_user: UserResponse, db: AsyncSession):
    platform = "twitter"
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

    postTweet()
