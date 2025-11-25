import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from app.models.platform_credentials import PlatformCredential
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse
from sqlalchemy import select, delete
import asyncio
from app.logger import setup_logger
from app.config import BACKEND_URI

logger = setup_logger(__name__)


CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/blogger"]
REDIRECT_URI = f"{BACKEND_URI}/api/auth/google/callback"

# def get_authorization_url():

# def postBlog(text):

#     creds = None

#     if os.path.exists("tokens.json"):
#         creds = Credentials.from_authorized_user_file('tokens.json', scopes=["https://www.googleapis.com/auth/blogger"])
        
#     if not creds or not creds.valid:
        
#         try:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 raise RefreshError("Invalid or missing refresh token")
        
#         except RefreshError:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'client_secret.json',
#                 scopes=["https://www.googleapis.com/auth/blogger"]
#             )

#             creds = flow.run_local_server(port=0)

#             with open("tokens.json", "w") as file:
#                 file.write(creds.to_json())

#     try:
#         service = build("blogger", "v3", credentials=creds)

#         blog_id = "3115491518418580833"

#         post_body = {
#             "kind": "blogger#post",
#             "blog":{
#                 "id": blog_id
#             },
#             "title": "Test Post",
#             "content": text,
#             "labels": ['test', 'first']
#         }
#         new_post = service.posts().insert(blogId = blog_id, body=post_body, isDraft=False).execute()

#         print(f"The new post is at url: {new_post['url']}")
        
#     except HttpError as error:
#         print(f"An error Occurred: {error}")

def get_authorization_url():
    # flow = Flow.from_client_secrets_file(
    #     CLIENT_SECRETS_FILE,
    #     scopes=SCOPES,
    #     redirect_uri=REDIRECT_URI
    # )
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    return flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="select_account"     # prompt="consent"
    )
    
        
async def save_credentials(request: Request, db: AsyncSession):
    
    user_id = request.session.get("user_id")
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials
    
    db.add(
        PlatformCredential(
            user_id=user_id,
            platform="google",
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            expires_at=credentials.expiry
        )
    )
    await db.commit()
    
    return credentials
        
async def postBlog(user_creds: PlatformCredential, text):   
   
    creds = Credentials(token=user_creds["access_token"], refresh_token=user_creds["refresh_token"])
    
    def blogger_sync():
        service = build("blogger", "v3", credentials=creds)
        
        blogs = service.blogs().listByUser(userId="self").execute()
        results = []        # for printing

        for blog in blogs.get("items", []):     # later give choice to choose the blogs
            blog_id = blog["id"]
            post_body = {
                "kind": "blogger#post",
                "title": "Test Post",
                "content": text,
                "labels": ['test', 'first']
            }
            new_post = service.posts().insert(blogId = blog_id, body=post_body, isDraft=False).execute()
            
            results.append(new_post['url'])
            
        return results
    
    try:
        urls = await asyncio.run_coroutine_threadsafe(blogger_sync)
        for url in urls:
            logger.info(f"The new post is at url: {url}")
        
    except HttpError as error:
        logger.error(f"An error Occurred: {error}")
    
        
async def check_status(current_user: UserResponse, db: AsyncSession):
    platform = "google"
    res = await db.scalars(select(PlatformCredential).where(
        (PlatformCredential.user_id == current_user.id) & 
        (PlatformCredential.platform == platform)
    ))
    results = res.all()    
    
    return {"integrated": len(results) > 0}

async def delete_user(current_user: UserResponse, db: AsyncSession):
    platform = "google"
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