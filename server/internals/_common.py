"""
Common functions and classes used by several modules in internals. Not meant to be used directly.
"""
# Standard Library Imports
from datetime import timedelta, datetime

# Third Party Imports
from jose import jwt


def _makeAccessToken(
        data: dict,
        expires: timedelta,
        secretKey: str
) -> tuple[str, datetime]:
    """
    Makes an access token.

    Args:
        data (dict): The data to include in the token.
        expires (timedelta): The time until the token expires.

    Returns:
        tuple[str, datetime]: The access token and the expiration time.
    """
    # Copy the data
    toEncode: dict = data.copy()

    # Add the expiration time
    expireTime = datetime.utcnow() + expires
    toEncode["exp"] = expireTime

    # Encode the token
    return (
        jwt.encode(
            toEncode,
            secretKey,
            algorithm="HS256"
        ),
        expireTime
    )
