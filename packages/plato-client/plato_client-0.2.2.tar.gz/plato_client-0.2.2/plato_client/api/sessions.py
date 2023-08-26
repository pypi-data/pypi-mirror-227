from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from plato_client.core.auth import PLATO_AUTH
from plato_client.core.models import AccessToken

sessions_api = APIRouter()


@sessions_api.post("/session/login", response_model=AccessToken)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login a user and return an access token.

    Description:
    - This endpoint is used to login a user and return an access token.
    - The access token is used to authenticate the user for all other endpoints.
    - The access token is sent in the header of all requests to the server.
    
    Args:
        form_data (OAuth2PasswordRequestForm, optional): [description]. Defaults to Depends().
        
    Returns:
        AccessToken: the access token for the user.
        
    Raises:
        HTTPException: if the user could not be authenticated.
        """
    try:
        tokens = await PLATO_AUTH.authenticate_user(
            form_data.username, form_data.password
        )

        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return AccessToken(access_token=tokens.access_token, token_type="bearer")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@sessions_api.post("/session/logout")
async def user_logout(token: str = Depends(PLATO_AUTH.get_user_info())):
    """
    Logout a user and revoke their access token.
    
    Description:
    - This endpoint is used to logout a user and revoke their access token.
    - The access token is used to authenticate the user for all other endpoints.
    - The access token is sent in the header of all requests to the server.
    
    Args:
        token (str, optional): [description]. Defaults to Depends(PLATO_AUTH.get_user_info()).
    
    Returns:
        Boolean: True if the access token was successfully revoked.
    
    Raises:
        HTTPException: if the access token could not be revoked.
    """
    try:
        success = await PLATO_AUTH.revoke_tokens(token)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to revoke tokens",
            )

        return True

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@sessions_api.post("/session/list")
async def list_sessions(token: str = Depends(PLATO_AUTH.get_user_info())):
    """
    List all active sessions for a user.

    Description:
    - This endpoint is used to list all active sessions for a user.
    - The access token is used to authenticate the user for all other endpoints.
    - The access token is sent in the header of all requests to the server.

    Args:
        token (str, optional): [description]. Defaults to Depends(PLATO_AUTH.get_user_info()).

    Returns:
        List[Session]: a list of all active sessions for the user.

    Raises:
        HTTPException: if the sessions could not be listed.
    """
    raise NotImplementedError()
