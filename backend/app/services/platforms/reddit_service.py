import os
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode
import secrets
from app.models.platform_credentials import PlatformCredential
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

REDIRECT_URI = "http://localhost:8000/auth/reddit/callback"

client_id = os.environ.get("reddit_client_ID")
client_secret = os.environ.get("reddit_client_secret")


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

    
def save_credentials(code, current_user, db):
    
    
    auth = HTTPBasicAuth(client_id, client_secret)
    headers = {"User-Agent": "web_app/0.1 by Ok_Turnip9330"}
        
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(url="https://www.reddit.com/api/v1/access_token", data=data, auth=auth, headers=headers)

    result = response.json()
    db.add(
        PlatformCredential(
            user_id=current_user.user_id,
            platform="google",
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            expires_at=result["expires_in"]
        )
    )
    

# response  = requests.get(url="https://oauth.reddit.com/api/v1/me", headers=headers)

# print(response.json())

# Compulsory keys for data. !!! Change "sr" to desired subreddit.
async def postReddit(db: AsyncSession, current_user, title = "New Post", text="Place_holder", sr="test"):
    
    credentials = await db.scalars(
        select(PlatformCredential).filter(PlatformCredential.platform == "reddit" & PlatformCredential.user_id==current_user.id)
    ).first()

    if credentials.expires_at < datetime.now()
    
    headers = {"User-Agent": "web_app/0.1 by Ok_Turnip9330"}
        
    data = {
        "grant_type": "refresh_token",
        "refresh_token": credentials.refresh_token
    }
    
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

    response = requests.post(
        "https://oauth.reddit.com/api/submit", 
        headers=headers,
        data=data
    )
    
    response.raise_for_status()

if __name__ == "__main__":  
# response.status_code()

    postReddit()
