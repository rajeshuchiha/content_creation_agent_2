import os
import httpx    
import asyncio
from urllib.parse import urlencode, parse_qs
import secrets
from app.models.platform_credentials import PlatformCredential
from app.schemas.user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from requests_oauthlib import OAuth1
from datetime import datetime, timedelta

REDIRECT_URI = "http://localhost:8000/api/auth/twitter/callback"

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
        
    data = parse_qs(res.text)

    oauth_token = data["oauth_token"][0]
    oauth_token_secret = data["oauth_token_secret"][0]    
        
    state = secrets.token_urlsafe(16)

    params = {
        "oauth_token": oauth_token
    }
  
    authorization_url = f"https://api.x.com/oauth/authorize?{urlencode(params)}"
    return authorization_url, state, oauth_token_secret

    
async def save_credentials(request, db: AsyncSession):
    
    user_id = request.session.get("user_id")
    token_secret = request.session.get("oauth_token_secret")
    oauth_token = request.query_params.get('oauth_token')
    oauth_verifier = request.query_params.get('oauth_verifier')
    
    oauth = OAuth1(
        oauth_consumer_key,
        oauth_consumer_key_secret,
        oauth_token,
        token_secret,
        verifier=oauth_verifier
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url="https://api.x.com/oauth/access_token", auth=oauth) 
        response.raise_for_status()

    credentials = parse_qs(response.text)
    
    access_token = credentials["oauth_token"][0]
    access_secret = credentials["oauth_token_secret"][0]
        
    db.add(
        PlatformCredential(
            user_id=user_id,
            platform="twitter",
            access_token=access_token,
            refresh_token=access_secret,    # Not refresh_token **Remember**
            expires_at=datetime.now + timedelta(days=365)   # Just placeholder
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

        
    oauth = OAuth1(
        oauth_consumer_key,
        oauth_consumer_key_secret,
        access_token,
        access_token_secret,
        signature_type="auth_header"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.twitter.com/2/tweets", 
                auth=oauth,
                json={"text": tweet}
            )

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
    
    return {"integrated": len(results) > 0}

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

    asyncio.run(postTweet(...))
