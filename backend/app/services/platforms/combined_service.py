from app.services.platforms import reddit_service, twitter_service
from app.schemas.content import Item
from sqlalchemy import select
from app.models.platform_credentials import PlatformCredential
from app.services.platforms import google_service, twitter_service
from app.logger import setup_logger

logger = setup_logger(__name__)

async def post(current_user, db, item: Item):
    user_id = current_user.id
    
    stmt = select(PlatformCredential).where(PlatformCredential.user_id == user_id)
    result = await db.scalars(stmt)
    creds = result.all()
    
    for cred in creds:
        
        try: 
            if cred.platform == "twitter":
                await twitter_service.postTweet(credentials=cred, tweet=item.tweet) #  Change later
        
            if cred.platform == "reddit":
                # Add a check function whether to refresh token
                cred = await reddit_service.check_access_token(cred, db)
                # reddit_post_dict = json.loads(item.reddit_post)
                if cred:
                    reddit_post_dict = item.reddit_post
                    await reddit_service.postReddit(credentials=cred, title=reddit_post_dict.title, text=reddit_post_dict.body)
                
            if cred.platform == "google":
                await google_service.postBlog(cred, db, item.blog_post)
    
        except Exception as e:
            logger.exception(f"Error: {e}")