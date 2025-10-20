from app.services.platforms import tweet_service, reddit_service, blogger_service
from app.schemas.content import Item
from sqlalchemy.sql import select
from app.models.platform_credentials import PlatformCredential
import json

async def post(current_user, db, item: Item):
    user_id = current_user.id
    
    creds = await db.scalars(select(PlatformCredential).filter(PlatformCredential.user_id == user_id)).all()
    
    for cred in creds:
        
        if cred.platform == "twitter":
            await tweet_service.postTweet(item.tweet) #  Change later
     
        if cred.platform == "reddit":
            reddit_post_dict = json.loads(item.reddit_post)
            await reddit_service.postReddit(db=db, current_user=current_user, title=reddit_post_dict['title'], text=reddit_post_dict['body'])
            
        if cred.platform == "blogger":
            await blogger_service.postBlog(cred, item.blog_post)
    