import json
import os
from typing import Union, Optional, List
from datetime import datetime
from pydantic import BaseModel


class AuthProviderConfig(BaseModel):
    """Auth Provider Config"""

    client_id: str = os.environ.get("AUTH_PROVIDER_APP_ID", default="")
    client_secret: str = os.environ.get("AUTH_PROVIDER_APP_SECRET", default="")
    domain: str = os.environ.get("AUTH_PROVIDER_DOMAIN", default="")
    plato_core_url: str = os.environ.get("PLATO_CORE_URL", default="")
    user_scope: dict = json.loads(
        os.environ.get("AUTH_PROVIDER_USER_SCOPE", default="{}")
    )
    app_scope: dict = json.loads(
        os.environ.get("AUTH_PROVIDER_APP_SCOPE", default="{}")
    )
    audience: str = os.environ.get("AUTH_PROVIDER_AUDIENCE", default="")


class AccessToken(BaseModel):
    """Access Token"""

    access_token: str
    token_type: str


class Tokens(BaseModel):
    """Tokens"""

    refresh_token: str
    access_token: str


class TokenData(BaseModel):
    """Token Data"""

    username: Union[str, None] = None


class PlatoUser(BaseModel):
    """Plato User"""

    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    given_name: Union[str, None] = None
    family_name: Union[str, None] = None
    userid: Union[str, None] = None


class PlatoUserWithPassword(PlatoUser):
    """Plato User With Password"""

    hashed_password: str
