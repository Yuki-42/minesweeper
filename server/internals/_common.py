"""
Common functions and classes used by several modules in internals. Not meant to be used directly.
"""
# Standard Library Imports
from datetime import timedelta, datetime

# Third Party Imports
from jose import jwt


def _makeAccessToken(
        config,  # This is not type hinted because it is a circular import
        data: dict,
        expires: timedelta = None
) -> str:
    """
    Makes an access token.

    Args:
        data (dict): The data to include in the token.
        expires (timedelta): The time until the token expires.

    Returns:
        str: The access token.
    """
    # Set the default expiration time
    expires = expires or timedelta(days=config.tokenExpireDays, minutes=config.tokenExpireMinutes)

    # Copy the data
    toEncode: dict = data.copy()

    # Add the expiration time
    toEncode["exp"] = datetime.utcnow() + expires

    # Encode the token
    return jwt.encode(
        toEncode,
        config.secretKey,
        algorithm="HS256"
    )
