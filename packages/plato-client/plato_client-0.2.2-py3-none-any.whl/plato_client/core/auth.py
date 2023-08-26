# import subprocess
from datetime import datetime, timedelta
from typing import Callable, Union

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from plato_client import CONFIG

from .models import *

ALGORITHM = CONFIG["auth.algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = CONFIG["auth.access_token_expiry_min"]
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -- helpers --
def _verify_password(plain_password, hashed_password) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): plain password
        hashed_password (str): hashed password

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.

    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def _get_password_hash(password) -> str:
    """
    Get the hashed version of a password.

    Args:
        password (str): password to hash

    Returns:
        str: hashed password
    """
    return PWD_CONTEXT.hash(password)


def _create_test_access_token(data: PlatoUser, expires_delta: timedelta = None):
    """
    Create a test access token. This is used for testing purposes primarily.

    Args:
        data (PlatoUser): user data
        expires_delta (timedelta, optional): expiry time. Defaults to None.

    Returns:
        str: access token
    """
    # def generate_random_hex_string():
    #     result = subprocess.run(
    #         ["openssl", "rand", "-hex", "32"],
    #         stdout=subprocess.PIPE,
    #         text=True,
    #         check=True,
    #     )
    #     return result.stdout.strip()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.dict()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    # secret_key = generate_random_hex_string()
    encoded_jwt = jwt.encode(
        to_encode, CONFIG["auth.test.secret_key"], algorithm=ALGORITHM
    )
    return encoded_jwt  #  ,secret_key


def decode_jwt(jwt_token: str, secret: str, audience: str = None) -> dict:
    """
    Decodes a JWT token and returns the payload.

    Args:
        jwt_token (str): JWT token
        secret (str): secret key
        audience (str, optional): audience. Defaults to None.

    Returns:
        dict: payload

    Raises:
        HTTPException: if the JWT token is invalid.

    """
    try:
        payload = jwt.decode(
            jwt_token,
            secret,
            algorithms=[ALGORITHM],
            audience=audience,
            options={"verify_signature": False},
        )
        return payload
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


class Plato_Auth:
    """
        Plato Auth

        These are the Oauth2 flows - Note client app refers to the app backend using the plato_client:
        1) Authorization Code Grant: [Implemented here]
            - most commonly used and secure flow
            - for server-side web applications, native apps, and mobile apps
            - user authenticates with the authorization server and gets an authorization code
            - client application  exchanges authorization code for an access token

        2) Implicit Grant:
            - used for client-side web applications (such as single-page apps)
            - access token is directly issued after user authentication
            * replaced by the Authorization Code Grant with PKCE due to security concerns

        3) Resource Owner Password Credentials (ROPC) Grant: [Implemented here]
            - used with trusted 1st-party apps
            - less secure
            - user provides their username and password directly to the client app
            - client app exchanges username+pwd for an access token.

        4) Client Credentials Grant:  [Implemented here]
            - used for server-to-server communication
            - client app needs to access protected resources on behalf of itself (not on behalf of user)
            - client authenticates with its own credentials and receives an access token directly

        5) Device Authorization Grant:
            - used in smart TVs or IoT devices
            - user authorizes the device using another device to obtain an access token

        6) Refresh Token Grant:
            - part of other flows (e.g Authorization Code Grant or ROPC Grant)
            - after access token expires client can use a refresh token to request a new access token without having the user to re-authenticate - who wants to reauthenticate again lol

        7) Extension Grants:
            - custom grant types for use cases not covered by above standard flows

    Purpose of this class is to abstract the complexity of authentication form client apps. It implements several flows as mentioned above.
    """

    def __init__(
        self, auth_provider_config: AuthProviderConfig = AuthProviderConfig()
    ) -> None:
        """Initialize the Plato Auth

        Args:
            auth_provider_config (AuthProviderConfig, optional): Auth provider config. Defaults to AuthProviderConfig().

        Note:
            - The auth provider config is used to configure the auth provider (e.g. Okta, Auth0, etc)
        """
        self.auth_provider_config = auth_provider_config
        self.oauth2_authorization_scheme = OAuth2AuthorizationCodeBearer(
            authorizationUrl=f"{self.auth_provider_config.domain}/oauth2/default/v1/authorize",
            tokenUrl=f"{self.auth_provider_config.domain}/oauth2/default/v1/token",
            refreshUrl=f"{self.auth_provider_config.domain}/oauth2/default/v1/token",
            scopes=self.auth_provider_config.user_scope,
        )
        self.provider_domain = self.auth_provider_config.domain
        # self.oauth2_client_credentials_scheme = OAuth2PasswordBearer(  # Todo: not used
        #     tokenUrl=f"{self.auth_provider_config.domain}/oauth2/default/v1/token"
        # )

    def _get_user_info_from_provider(self, access_token: str) -> PlatoUser:
        """
        Gets the user info from the auth provider (e.g., Okta).

        Args:
            access_token (str): access token

        Returns:
            PlatoUser: user info

        Raises:
            HTTPException: if the user info cannot be retrieved from the auth provider.
        """

        userinfo_url = f"{self.auth_provider_config.domain}/oauth2/default/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = httpx.get(userinfo_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        res = response.json()
        return PlatoUser(
            username=res["name"],
            email=res["email"],
            full_name=res["name"],
            given_name=res["given_name"],
            family_name=res["family_name"],
            userid=res["sub"],
        )

    def _get_user_info_from_jwt_token(self, access_token: str) -> PlatoUser:
        """
        Decodes the JWT token and returns the user info (locally).

        Args:
            access_token (str): access token

        Returns:
            PlatoUser: user info

        Raises:
            HTTPException: if the JWT token is invalid.

        """

        try:
            res = decode_jwt(
                access_token,
                self.auth_provider_config.client_secret,
                audience=self.auth_provider_config.audience,
            )
            return PlatoUser(
                username=res["name"],
                email=res["email"],
                full_name=res["name"],
                userid=res["sub"],
            )
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
            )

    def get_user_info(self, use_provider: bool = True) -> Callable:
        """
        Returns the user info using the access token.

        Args:
            use_provider (bool, optional): whether to use the auth provider to get the user info. Defaults to True.

        Returns:
            Callable: function that returns the user info.

        """

        async def _get_user_info(request: Request, access_token: str = None) -> dict:
            if access_token is None:  # extract from the request
                access_token = await self.oauth2_authorization_scheme(request)
            else:
                pass  # access_token explicitly passed in
            return (
                self._get_user_info_from_provider(access_token)
                if use_provider
                else self._get_user_info_from_jwt_token(access_token)
            )

        return _get_user_info

    # -- Authorization Code Flow --

    def refresh_token(self, refresh_token: str) -> Tokens:
        """
        Refreshes an access token using the given refresh token.

        Args:
            refresh_token (str): refresh token

        Returns:
            Tokens: access token and refresh token

        Raises:
            HTTPException: if the refresh token is invalid or expired.
        """
        token_url = f"{self.auth_provider_config.domain}/oauth2/default/v1/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.auth_provider_config.client_id,
            "client_secret": self.auth_provider_config.client_secret,
            "refresh_token": refresh_token,
        }
        response = httpx.post(token_url, data=payload, headers=headers)
        response.raise_for_status()
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        res = response.json()
        return Tokens(
            access_token=res["access_token"], refresh_token=res["refresh_token"]
        )

    # -- Client Credentials Flow --

    def get_token_client_credentials(self) -> AccessToken:
        """
        Gets an access token using the client credentials flow.

        Returns:
            AccessToken: access token

        Raises:
            HTTPException: if the access token cannot be retrieved.
        """
        token_url = f"{self.auth_provider_config.domain}/oauth2/default/v1/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.auth_provider_config.client_id,
            "client_secret": self.auth_provider_config.client_secret,
            "scope": self.auth_provider_config.app_scope,
        }
        # !! Todo: set verify to True in production env !!
        response = httpx.post(
            token_url,
            data=payload,
            headers=headers,
            follow_redirects=True,
            verify=False,  # verify=True
        )

        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return AccessToken(
            access_token=response.json()["access_token"], token_type="bearer"
        )

    # -- Resource Owner Password Credentials (ROPC) Grant Flow --
    async def authenticate_user(self, username: str, password: str) -> Tokens:
        """
        Authenticates a user using the resource owner password credentials flow.

        Args:
            username (str): username
            password (str): password

        Returns:
            Tokens: access token and refresh token; None if the authentication fails.

        """
        token_url = f"{self.auth_provider_config.domain}/oauth2/default/v1/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "password",
            "client_id": self.auth_provider_config.client_id,
            "client_secret": self.auth_provider_config.client_secret,
            "username": username,
            "password": password,
            "scope": self.auth_provider_config.user_scope,
        }
        response = httpx.post(token_url, data=payload, headers=headers)

        if response.status_code != 200:
            return None

        res = response.json()
        return Tokens(
            access_token=res["access_token"], refresh_token=res["refresh_token"]
        )

    async def revoke_tokens(self, token: str) -> bool:
        """
        Revokes the given token.

        Args:
            token (str): token to revoke

        Returns:
            bool: whether the token is revoked successfully.

        """
        revoke_url = f"{self.auth_provider_config.domain}/oauth2/default/v1/revoke"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "token": token,
            "client_id": self.auth_provider_config.client_id,
            "client_secret": self.auth_provider_config.client_secret,
        }
        response = httpx.post(revoke_url, data=payload, headers=headers)

        return response.status_code == 200


# Initialize the Auth helper with the config file
PLATO_AUTH = Plato_Auth()


async def get_access_token(request: Request) -> str:
    """
    Get access token from cache or get a new one if not cached or expired

    Args:
        request (Request): FastAPI request object

    Returns:
        str: access token

    """
    # check if token cached & not expired
    cached_token = request.app.state.access_token
    cached_token_expire_time = request.app.state.access_token_expire_time

    if cached_token and cached_token_expire_time > datetime.utcnow():
        # ok found in cache
        return cached_token

    #  get a new token
    access_token = await PLATO_AUTH.get_token_client_credentials()
    expire_time = datetime.utcnow() + timedelta(seconds=access_token.expires_in)

    # cache it
    request.app.state.access_token = access_token.access_token
    request.app.state.access_token_expire_time = expire_time

    return access_token.access_token


def get_auth_headers(token: str) -> dict:
    """
    Get authorization headers for HTTP requests

    Args:
        token (str): access token

    Returns:
        dict: authorization headers

    """
    return {
        "Authorization": f"Bearer {token}",
    }
