from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException
import asyncio
from fastapi.responses import RedirectResponse
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.platforms import twitter_service
from app.services import auth_service
from app.schemas.user import UserResponse
from app.config import FRONTEND_URI

REDIRECT_URI=f"{FRONTEND_URI}/dashboard"

router = APIRouter(
    prefix="/api/auth/twitter", 
    tags=["twitter OAuth"],
    # dependencies=[Depends(auth_service.get_current_active_user)]
)

@router.get("/authorize")
async def authorize(request: Request, current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)]):
    authorization_url = await asyncio.to_thread(twitter_service.get_authorization_url)  # function name as arg 
    # request.session["state"] = state  # store for CSRF protection
    request.session["user_id"] = current_user.id
    
    return {"auth_url": authorization_url}


@router.get("/callback")
async def oauth2callback(request: Request, db: AsyncSession = Depends(get_db)):
    # saved_state = request.session.get("state")
    # received_state = request.query_params.get("state")

    # if saved_state != received_state:
    #     return HTTPException(400, "Invalid session state")
    
    await twitter_service.save_credentials(request, db)  

    return RedirectResponse(url=REDIRECT_URI, status_code=302)

@router.get("/status")
async def getStatus(current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], db: AsyncSession = Depends(get_db)):
    
    return await twitter_service.check_status(current_user, db)

@router.delete("/user")
async def delete_user(current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], db: AsyncSession = Depends(get_db)):
    
    return await twitter_service.delete_user(current_user, db)