import logging

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from plato_client.core.auth import PLATO_AUTH, get_access_token, get_auth_headers

logger = logging.getLogger(__name__)

users_api = APIRouter()

# NOTE: you need to initilaize the state access tokens in your Fastapi app as follows (or we can leverage alternative caching)
# app.state.access_token = None
# app.state.access_token_expire_time = None


# Add a new user
@users_api.post("/user/add_user")
async def add_user(
    app_id: str, user_info: dict, password: str, token: str = Depends(get_access_token)
):
    """
    This endpoint is used to add a new user to the system.

    Args:
        app_id (str): the ID of the app to add the user to.
        user_info (dict): the user's profile information.
        password (str): the user's password.
        token (str, optional): [description]. Defaults to Depends(get_access_token).

    Returns:
        json: the user's profile information.

    Raises:
        HTTPException:  if the user could not be added.
    
    """
    logger.info("Adding new user...")
    headers = {"Content-Type": "application/json", **get_auth_headers(token)}
    api_url = f"{PLATO_AUTH.provider_domain}/api/v1/users/{app_id}?activate=true"
    user_data = {
        "profile": user_info,
        "credentials": {"password": {"value": password}},
    }
    response = requests.post(api_url, json=user_data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return response.json()



@users_api.get("/user/{user_id}")
async def get_user(app_id: str, user_id: str, token: str = Depends(get_access_token)):
    """
    This endpoint is used to get a user's profile by user ID.

    Args:
        app_id (str): the ID of the app to get the user from.
        user_id (str): the ID of the user to get.
        token (str, optional): [description]. Defaults to Depends(get_access_token).

    Returns:    
        json: the user's profile information.

    Raises: 
        HTTPException:  if the user could not be found.
    
    """
    logger.info(msg=f"Getting user with ID: {user_id}")
    api_url = f"{PLATO_AUTH.provider_domain}/api/v1/users/{app_id}/{user_id}"
    response = requests.get(api_url, headers=get_auth_headers(token))

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return response.json()


@users_api.put("/user/{user_id}")
async def update_user(
    app_id: str, user_id: str, user_info: dict, token: str = Depends(get_access_token)
):
    """
    This endpoint is used to update a user's profile by user ID.

    Args:
        app_id (str): the ID of the app to update the user in.
        user_id (str): the ID of the user to update.
        user_info (dict): the user's profile information.
        token (str, optional): [description]. Defaults to Depends(get_access_token).
    
    Returns:
        json: the user's profile information.

    Raises: 
        HTTPException [400]:  if the user could not be updated.
    
    """
    logger.info(msg=f"Updating user with ID: {user_id}")
    api_url = f"{PLATO_AUTH.provider_domain}/api/v1/users/{app_id}/{user_id}"
    headers = {"Content-Type": "application/json", **get_auth_headers(token)}
    response = requests.put(api_url, json=user_info, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update user"
        )

    return response.json()


@users_api.delete("/user/{user_id}")
async def delete_user(
    app_id: str, user_id: str, token: str = Depends(get_access_token)
):
    """
    This endpoint is used to delete a user by user ID.

    Args:
        app_id (str): the ID of the app to delete the user from.
        user_id (str): the ID of the user to delete.
        token (str, optional): [description]. Defaults to Depends(get_access_token).

    Returns:
        json: the user's profile information.

    Raises: 
        HTTPException [400]: if the user could not be deleted.
    
    """
    logger.info(msg=f"Deleting user with ID: {user_id}")
    api_url = f"{PLATO_AUTH.provider_domain}/api/v1/users/{app_id}/{user_id}"
    headers = get_auth_headers(token)
    response = requests.delete(api_url, headers=headers)

    if response.status_code != 204:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete user"
        )

    return {"detail": "User deleted successfully"}


# Reset a user's password by user ID
@users_api.post("/user/{user_id}/reset_password")
async def reset_password(
    app_id: str, user_id: str, new_password: str, token: str = Depends(get_access_token)
):
    """
    This endpoint is used to reset a user's password by user ID.


    Args:
        app_id (str): the ID of the app to reset the user's password in.
        user_id (str): the ID of the user to reset the password for.
        new_password (str): the user's new password.
        token (str, optional): [description]. Defaults to Depends(get_access_token).

    Returns:
        json: the user's profile information.

    Raises:
        HTTPException [400]:  if the password could not be reset.
    
    """
    logger.info(msg=f"Resetting password for user with ID: {user_id}")
    api_url = f"{PLATO_AUTH.provider_domain}/api/v1/users/{user_id}/{app_id}/credentials/password"
    headers = {"Content-Type": "application/json", **get_auth_headers(token)}
    password_data = {"password": new_password}
    response = requests.post(api_url, json=password_data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update password"
        )

    return {"detail": "Password reset successfully"}
