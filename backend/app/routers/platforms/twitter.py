from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.platforms import twitter_service
from app.services import auth_service
from app.schemas.user import UserResponse

FRONTEND_URL= "http://localhost:3000"

router = APIRouter(
    prefix="/api/auth/twitter", 
    tags=["twitter OAuth"],
    # dependencies=[Depends(auth_service.get_current_active_user)]
)

@router.get("/authorize")
async def authorize(request: Request, current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)]):
    authorization_url, state, oauth_token_secret = await twitter_service.get_authorization_url()
    request.session["state"] = state  # store for CSRF protection
    request.session["user_id"] = current_user.id
    request.session["oauth_token_secret"] = oauth_token_secret
    
    return {"auth_url": authorization_url}


@router.get("/callback")
async def oauth2callback(request: Request, db: AsyncSession = Depends(get_db)):
    saved_state = request.session.get("state")
    received_state = request.query_params.get("state")

    if saved_state != received_state:
        return HTTPException(400, "Invalid session state")
    
    credentials = await twitter_service.save_credentials(request, db)

    return RedirectResponse(url=f"{FRONTEND_URL}/dashboard", status_code=302)

@router.get("/status")
async def getStatus(current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], db: AsyncSession = Depends(get_db)):
    
    return await twitter_service.check_status(current_user, db)

@router.delete("/user")
async def delete_user(current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], db: AsyncSession = Depends(get_db)):
    
    return await twitter_service.delete_user(current_user, db)