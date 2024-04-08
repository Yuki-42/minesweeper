"""
Custom implementation of the built-in list data type.
"""

# Standard Library Imports
from datetime import datetime, timedelta

# Third Party Imports
from psycopg2.extensions import connection as Connection
from psycopg2.extras import RealDictRow, RealDictCursor

# Local Imports
from .token import Token
from ..._common import _makeAccessToken


class Tokens(list):
    """
    Custom implementation of the built-in list data type to store tokens.
    """
    # Type hints
    _connection: Connection
    _expirationTime: timedelta
    _userId: int
    _email: str

    def __init__(
            self,
            rows: list[RealDictRow],
            connection: Connection,
            expirationTime: timedelta,
            jwtSecret: str,
            userId: int,
            email: str
    ) -> None:
        """
        Initializes the Tokens object.

        Args:
            rows (list[RealDictRow]): The rows from the database.
            connection (Connection): The connection to use for database operations.
            expirationTime (timedelta): The time until the token expires.
            jwtSecret (str): The secret to use for the JWT.
            userId (int): The ID of the user.
            email (str): The email of the user.

        Returns:
            None
        """
        super().__init__()

        # Set the connection
        self._connection = connection
        self._expirationTime = expirationTime
        self._jwtSecret = jwtSecret
        self._userId = userId
        self._email = email

        for row in rows:
            self.append(Token(row, connection))

    def dict(self) -> list[dict]:
        """
        Returns the tokens as a list of dictionaries.

        Returns:
            list[dict]: The tokens as a list of dictionaries.
        """

        return [token.dict() for token in self]

    def refresh(self) -> None:
        """
        Refreshes all the tokens in the list to ensure that they are valid both in the database and in memory.

        Returns:
            None
        """
        # Get the current time
        currentTime: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Refresh all the tokens in the list
        for token in self:
            if token.expiration < currentTime:
                self.pop(self.index(token))  # Remove the token from the list

        # Remove old tokens from the database
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE FROM tokens
                WHERE user_id = %s
                AND expires_at < %s
                """,
                (self._userId, currentTime)
            )
            self._connection.commit()

    def new(self) -> Token:
        """
        Creates a new token and appends it to the list.

        Returns:
            Token: The new token.
        """

        # Create the new token
        accessToken, expires = _makeAccessToken(
            {
                "sub": self._email
            },
            self._expirationTime,
            self._jwtSecret
        )

        # Add the token to the database
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO tokens (user_id, token, expires_at)
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (self._userId, accessToken, expires)
            )
            row: RealDictRow = cursor.fetchone()
            self._connection.commit()

        # Create the token object
        token: Token = Token(row, self._connection)

        # Append the token to the list
        self.append(token)

        return token
