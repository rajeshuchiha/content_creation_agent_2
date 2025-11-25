import os
import httpx    
import asyncio
from urllib.parse import urlencode, parse_qs
import secrets
from app.models.platform_credentials import PlatformCredential
from app.schemas.user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime, timedelta
import tweepy
from app.logger import setup_logger
from app.config import BACKEND_URI

logger = setup_logger(__name__)

REDIRECT_URI = f"{BACKEND_URI}/api/auth/twitter/callback"

oauth_consumer_key = os.environ.get("twitter_API_key")
oauth_consumer_key_secret = os.environ.get("twitter_API_key_secret")

# class CustomAuth(httpx.Auth):
#     def __init__(self, consumer_key, consumer_secret, 
#                  access_token=None, access_token_secret=None,
#                  callback_uri=None, verfier=None):
#         self.consumer_key = consumer_key
#         self.consumer_secret = consumer_secret
#         self.token = access_token
#         self.token_secret = access_token_secret or ""
#         self.callback_uri = callback_uri
#         self.verifier = verfier
        
#     def auth_flow(self, request):
        
#         request

oauth1_user_handler = tweepy.OAuth1UserHandler(
    consumer_key=oauth_consumer_key,
    consumer_secret=oauth_consumer_key_secret,
    callback=REDIRECT_URI
)

def get_authorization_url():
    
    authorization_url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)
    
    return authorization_url

    
async def save_credentials(request, db: AsyncSession):
    
    user_id = request.session.get("user_id")
    oauth_token = request.query_params.get('oauth_token')
    oauth_verifier = request.query_params.get('oauth_verifier')
    
    access_token, access_secret = await asyncio.to_thread(oauth1_user_handler.get_access_token, oauth_verifier)  # function name and its args as arg 
        
    db.add(
        PlatformCredential(
            user_id=user_id,
            platform="twitter",
            access_token=access_token,
            refresh_token=access_secret,    # Not refresh_token **Remember**
            expires_at=datetime.now() + timedelta(days=365)   # Just placeholder
        )
    )
    await db.commit()


async def postTweet(credentials: PlatformCredential, tweet):

    access_token = credentials.access_token
    access_secret = credentials.refresh_token
    
    if not tweet:
        print("Twitter post has NULL tweet.")
        return  

    client = tweepy.Client(
        consumer_key=oauth_consumer_key,
        consumer_secret=oauth_consumer_key_secret,
        access_token=access_token,
        access_token_secret=access_secret   
    )

    try:
        response = client.create_tweet(text=tweet)
        logger.info("Tweet posted! ID:", response.data["id"])
            
    except Exception as e:
        logger.error(f"Twitter Request failed: {e}")
            
            
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
