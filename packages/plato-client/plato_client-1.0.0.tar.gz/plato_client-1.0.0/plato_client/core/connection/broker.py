"""Module containing broker connection logic"""
from enum import Enum

from plato_client import CONFIG


class PlatoEnvironment(str, Enum):
    """
    Defines the environment to connect to the Plato broker
    """

    LOCAL = "local"
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"

    @classmethod
    def list(cls):
        """Get list of values"""
        return list(map(lambda c: c.value, cls))


def get_base_url(env: PlatoEnvironment) -> str:
    """
    Get base url for the given environment. This is used to connect to the Palto broker.
    
    Args:
        env (PlatoEnvironment): Environment to get base url for
        
    Returns:
        str: base url for the given environment
        
    Raises:
        ValueError: if the environment is not one of PlatoEnvironment
    """
    url_config = CONFIG["broker"]["url"]
    if env == PlatoEnvironment.LOCAL:
        return url_config["local"]
    elif env == PlatoEnvironment.DEVELOPMENT:
        return url_config["dev"]
    elif env == PlatoEnvironment.PRODUCTION:
        return url_config["prod"]
    else:
        raise ValueError(
            f"'env' value should be one of {PlatoEnvironment.list()}, provided: {env}"
        )
