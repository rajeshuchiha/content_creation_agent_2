from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.services.platforms import google_service
from app.services import auth_service
from app.schemas.user import UserResponse

FRONTEND_URL= "http://localhost:5173"

router = APIRouter(
    prefix="/auth/google", 
    tags=["google OAuth"],
    dependencies=[Depends(auth_service.get_current_active_user)]
)

@router.get("/authorize")
def authorize(request: Request):
    authorization_url, state = google_service.get_authorization_url()
    request.session["state"] = state  # store for CSRF protection
    return RedirectResponse(authorization_url)


@router.get("/callback")
def oauth2callback(request: Request, current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], db: AsyncSession = Depends(get_db)):
    saved_state = request.session.get("state")
    received_state = request.query_params.get("state")

    if saved_state != received_state:
        return {"error": "Invalid state parameter"}

    credentials = google_service.save_credentials(request, current_user, db)

    # You could store credentials.token in DB here
    return RedirectResponse(url=f"{FRONTEND_URL}/dashboard")

@router.get("/me")
async def getStatus(current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], db: AsyncSession = Depends(get_db)):
    
    return await google_service.check_status(current_user, db)

@router.delete("/user")
async def delete_user(current_user: Annotated[UserResponse, Depends(auth_service.get_current_active_user)], db: AsyncSession = Depends(get_db)):
    
    return await google_service.delete_user(current_user, db)