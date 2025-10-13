from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from ...models.user import User
from ...database import get_db
from sqlalchemy.orm import Session
from ...services.platforms import blogger_service

router = APIRouter(prefix="/auth/google", tags=["Google OAuth"])

@router.get("/authorize")
def authorize(request: Request):
    # flow = Flow.from_client_secrets_file(
    #     CLIENT_SECRETS_FILE,
    #     scopes=SCOPES,
    #     redirect_uri=REDIRECT_URI
    # )
    # authorization_url, state = flow.authorization_url(
    #     access_type="offline",
    #     include_granted_scopes="true",
    #     # prompt="consent"
    # )
    authorization_url, state = blogger_service.get_authorization_url()
    request.session["state"] = state  # store for CSRF protection
    return RedirectResponse(authorization_url)


@router.get("/callback")
def oauth2callback(request: Request, user_id: int, db: Session = Depends(get_db)):
    saved_state = request.session.get("state")
    received_state = request.query_params.get("state")

    if saved_state != received_state:
        return {"error": "Invalid state parameter"}

    credentials = blogger_service.save_credentials(request, user_id, db)

    # You could store credentials.token in DB here
    return {"message": "Authorization successful!", "access_token": credentials.token}
