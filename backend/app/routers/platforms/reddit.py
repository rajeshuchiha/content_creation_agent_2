from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.platforms import reddit_service
from app.services import auth_service
from app.schemas.user import UserResponse

FRONTEND_URL= "http://localhost:5173"

router = APIRouter(
    prefix="/api/auth/reddit", 
    tags=["Reddit OAuth"],
    dependencies=[Depends(auth_service.get_current_active_user)]
)

@router.get("/authorize")
def authorize(request: Request):
    authorization_url, state = reddit_service.get_authorization_url()
    request.session["state"] = state  # store for CSRF protection
    return RedirectResponse(authorization_url)


@router.get("/callback")
async def oauth2callback(request: Request, current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], db: AsyncSession = Depends(get_db)):
    saved_state = request.session.get("state")
    received_state = request.query_params.get("state")

    if saved_state != received_state:
        return {"error": "Invalid state parameter"}
    
    code = request.query_params.get('code')
    credentials = await reddit_service.save_credentials(code, current_user, db)

    return RedirectResponse(url=f"{FRONTEND_URL}/dashboard")

@router.get("/me")
async def getStatus(current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], db: AsyncSession = Depends(get_db)):
    
    return await reddit_service.check_status(current_user, db)