from app.services.platforms import reddit_service, twitter_service
from app.schemas.content import Item
from sqlalchemy import select
import json
from app.models.platform_credentials import PlatformCredential
from app.services.platforms import google_service, twitter_service

async def post(current_user, db, item: Item):
    user_id = current_user.id
    
    creds = await db.scalars(select(PlatformCredential).filter(PlatformCredential.user_id == user_id)).all()
    
    for cred in creds:
        
        if cred.platform == "twitter":
            await twitter_service.postTweet(credentials=cred, tweet=item.tweet) #  Change later
     
        if cred.platform == "reddit":
            # Add a check function whether to refresh token
            reddit_post_dict = json.loads(item.reddit_post)
            await reddit_service.postReddit(db=db, credentials=cred, title=reddit_post_dict['title'], text=reddit_post_dict['body'])
            
        if cred.platform == "blogger":
            await google_service.postBlog(cred, item.blog_post)
    