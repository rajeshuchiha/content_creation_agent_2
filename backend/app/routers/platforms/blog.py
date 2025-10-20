from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.platforms import blogger_service

router = APIRouter(prefix="/auth/google", tags=["Google OAuth"])

@router.get("/authorize")
def authorize(request: Request):
    authorization_url, state = blogger_service.get_authorization_url()
    request.session["state"] = state  # store for CSRF protection
    return RedirectResponse(authorization_url)


@router.get("/callback")
def oauth2callback(request: Request, user_id: int, db: AsyncSession = Depends(get_db)):
    saved_state = request.session.get("state")
    received_state = request.query_params.get("state")

    if saved_state != received_state:
        return {"error": "Invalid state parameter"}

    credentials = blogger_service.save_credentials(request, user_id, db)

    # You could store credentials.token in DB here
    return {"message": "Authorization successful!", "access_token": credentials.token}
