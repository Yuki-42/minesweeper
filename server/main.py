"""
Main file for the project
"""
from datetime import timedelta, datetime
# Standard Library Imports
from json import load as jsonLoad
from typing import Any, Annotated

# Third Party Imports
from fastapi import FastAPI, APIRouter, Response, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# Local Imports
from internals import Config, Database
from internals.datatypes.db import User, Game
from internals.logging import createLogger, SuppressedLoggerAdapter

# Create the FastAPI app
app: FastAPI = FastAPI()

# Create the OAuth2 password bearer
oauth2Scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

# Create the internals objects
config: Config = Config()
database: Database = Database(config)
logger: SuppressedLoggerAdapter = createLogger(
    "Main",
    databaseConnection=database.connection
)

# Constants
SECRET_KEY: str = config.secretKey
ACCESS_TOKEN_EXPIRE: timedelta = timedelta(days=config.tokenExpireDays, minutes=config.tokenExpireMinutes)

"""
================================================================================================================================================================
    Miscellaneous Functions
================================================================================================================================================================
"""


async def currentUser(token: Annotated[str, Depends(oauth2Scheme)]) -> User | None:
    """
    Returns the current user.

    Args:
        token (str): The token for the user.

    Returns:
        User: The current user.
    """
    # Ensure that the token is valid
    if token is None:
        return None

    # Prepare the error message
    tokenError: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Decode the token
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise tokenError
    except JWTError:
        raise tokenError

    user: User = database.getUser(token=token)

    if not user:
        raise tokenError

    if user.banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is banned."
        )

    return user


def makeAccessToken(
        data: dict,
        expires: timedelta
) -> str:
    """
    Makes an access token.

    Args:
        data (dict): The data to include in the token.
        expires (timedelta): The time until the token expires.

    Returns:
        str: The access token.
    """
    # Copy the data
    toEncode: dict = data.copy()

    # Add the expiration time
    toEncode["exp"] = datetime.utcnow() + expires

    # Encode the token
    return jwt.encode(toEncode, config.secretKey, algorithm="HS256")


"""
================================================================================================================================================================
    Routes
================================================================================================================================================================
"""


@app.options("/")
@app.get("/")
async def _spec() -> dict[str, Any]:
    """
    Returns the OpenAPI specification.

    Returns:
        dict[str, str]: The OpenAPI specification.
    """
    return app.openapi()


"""
========================================================================================================================
    Game Routes
========================================================================================================================
"""


@app.get("/game", status_code=200)
async def _getGame(
        response: Response,
        user: Annotated[User, Depends(currentUser)],
        gameId: int = None,
        uuid: str = None,
) -> dict[str, Any]:
    """
    Returns the game with the given ID.

    Args:
        response (Response): The response object.
        user (User): The current user.
        gameId (int): The ID of the game.
        uuid (str): The UUID of the game.

    Returns:
        dict[str, Any]: The game.
    """
    # Ensure that only one of gameId or uuid is set
    if gameId is not None and uuid is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Only one of gameId or uuid may be set."}

    # Get the game
    game: Game | None = database.getGame(gameId, uuid)

    # Return the game
    if game is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Game not found."}

    return game.dict()


"""
========================================================================================================================
    User Routes
========================================================================================================================
"""


@app.post("/token", status_code=200)
async def _loginUser(
        formData: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response
) -> dict[str, Any]:
    """
    Logs in the user.

    Args:
        formData (OAuth2PasswordRequestForm): The form data.
        response (Response): The response object.

    Returns:
        dict[str, Any]: The user.
    """
    # Get the user
    user: User | None = database.getUser(email=formData.username)

    # Check if the user exists
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Check the password
    if not user.checkPassword(formData.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    #

    return {"access_token": user.accessToken, "token_type": "bearer"}


@app.get("/user", status_code=200)
async def _getUser(
        response: Response,
        user: Annotated[User, Depends(currentUser)],
        userId: int = None,
        uuid: str = None,
        email: str = None
) -> dict[str, Any]:
    """
    Returns the user with the given ID.

    Args:
        response (Response): The response object.
        user (User): The current user.
        userId (int): The ID of the user.
        uuid (str): The UUID of the user.
        email (str): The email of the user.

    Returns:
        dict[str, Any]: The user.
    """
    # Ensure that only one of userId, uuid, or email is set
    if userId is not None and uuid is not None and email is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Only one of userId, uuid, or email may be set."}

    # Ensure that the user is authorized to view the user
    if "read:user" not in user.oauthScopes and "all" not in user.oauthScopes:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"error": "Unauthorized"}

    # Get the user
    user: User = database.getUser(
        userId,
        uuid,
        email
    )

    # Return the user
    if user is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "User not found."}

    return user.dict()


@app.post("/user", status_code=200)
async def _createUser(
        response: Response,
        email: str,
        password: str,
        username: str
) -> dict[str, Any]:
    """
    Creates a new user.

    Args:
        response (Response): The response object.
        email (str): The email of the user.
        password (str): The password of the user.
        username (str): The username of the user.

    Returns:
        dict[str, Any]: The authentication token.
    """
    # Ensure password is at least 8 characters
    if len(password) < 8:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Password must be at least 8 characters."}

    # Ensure that at least 1 of each type of character is in the password
    if not any(char.isdigit() for char in password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Password must contain at least 1 number."}

    if not any(char.islower() for char in password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Password must contain at least 1 lowercase letter."}

    if not any(char.isupper() for char in password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Password must contain at least 1 uppercase letter."}

    if not any(char.isascii() for char in password):  # This might not work as expected
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Password must contain at least 1 special character."}

    # Create the user
    user: User = database.addUser(
        email,
        password,
        username
    )

    # Return the user's access token
    return {"access_token": user.accessToken, "token_type": "bearer"}
