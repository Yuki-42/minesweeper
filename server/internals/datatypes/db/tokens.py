"""
Custom implementation of the built-in list data type.
"""

# Standard Library Imports
from datetime import datetime, timedelta
from typing import Iterator

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
        # Refresh the tokens before returning them
        self._refresh()
        return [token.dict() for token in self]

    def _refresh(self) -> None:
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
        # Refresh the tokens before creating a new one
        self._refresh()

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

    """
===============================================================================================================================================================
        Builtin Method Overrides
===============================================================================================================================================================
    """

    def __getitem__(self, key: int) -> Token:
        """
        Returns the token at the given index.

        Args:
            key (int): The index of the token.

        Returns:
            Token: The token at the given index.
        """
        # Refresh the tokens before returning them
        self._refresh()
        return super().__getitem__(key)

    def __iter__(self) -> Iterator:
        """
        Returns the iterator for the tokens.

        Returns:
            Tokens: The iterator for the tokens.
        """
        # Refresh the tokens before returning them
        self._refresh()
        return super().__iter__()

    def __len__(self) -> int:
        """
        Returns the number of tokens in the list.

        Returns:
            int: The number of tokens in the list.
        """
        # Refresh the tokens before returning them
        self._refresh()
        return super().__len__()

    def __contains__(self, token: Token) -> bool:
        """
        Checks if the list contains the given token.

        Args:
            token (Token): The token to check for.

        Returns:
            bool: True if the token is in the list, False otherwise.
        """
        # Refresh the tokens before checking for the token
        self._refresh()
        return super().__contains__(token)

    def __str__(self) -> str:
        """
        Returns the string representation of the tokens.

        Returns:
            str: The string representation of the tokens.
        """
        # Refresh the tokens before returning them
        self._refresh()
        return super().__str__()

    def __repr__(self) -> str:
        """
        Returns the string representation of the tokens.

        Returns:
            str: The string representation of the tokens.
        """
        # Refresh the tokens before returning them
        self._refresh()
        return super().__repr__()

    def __eq__(self, other: list[Token]) -> bool:
        """
        Checks if the list of tokens is equal to the other list of tokens.

        Args:
            other (list[Token]): The other list of tokens.

        Returns:
            bool: True if the lists are equal, False otherwise.
        """
        # Refresh the tokens before checking for equality
        self._refresh()
        return super().__eq__(other)

    def __ne__(self, other: list[Token]) -> bool:
        """
        Checks if the list of tokens is not equal to the other list of tokens.

        Args:
            other (list[Token]): The other list of tokens.

        Returns:
            bool: True if the lists are not equal, False otherwise.
        """
        # Refresh the tokens before checking for inequality
        self._refresh()
        return super().__ne__(other)

    def __lt__(self, other: list[Token]) -> bool:
        """
        Checks if the list of tokens is less than the other list of tokens.

        Args:
            other (list[Token]): The other list of tokens.

        Returns:
            bool: True if the list is less than the other list, False otherwise.
        """
        # Refresh the tokens before checking for less than
        self._refresh()
        return super().__lt__(other)

    def __le__(self, other: list[Token]) -> bool:
        """
        Checks if the list of tokens is less than or equal to the other list of tokens.

        Args:
            other (list[Token]): The other list of tokens.

        Returns:
            bool: True if the list is less than or equal to the other list, False otherwise.
        """
        # Refresh the tokens before checking for less than or equal to
        self._refresh()
        return super().__le__(other)

    def __gt__(self, other: list[Token]) -> bool:
        """
        Checks if the list of tokens is greater than the other list of tokens.

        Args:
            other (list[Token]): The other list of tokens.

        Returns:
            bool: True if the list is greater than the other list, False otherwise.
        """
        # Refresh the tokens before checking for greater than
        self._refresh()
        return super().__gt__(other)

    def __ge__(self, other: list[Token]) -> bool:
        """
        Checks if the list of tokens is greater than or equal to the other list of tokens.

        Args:
            other (list[Token]): The other list of tokens.

        Returns:
            bool: True if the list is greater than or equal to the other list, False otherwise.
        """
        # Refresh the tokens before checking for greater than or equal to
        self._refresh()
        return super().__ge__(other)

    def __add__(self, other: list[Token]) -> list[Token]:
        """
        Adds the other list of tokens to the list of tokens.

        Args:
            other (list[Token]): The other list of tokens.

        Returns:
            list[Token]: The combined list of tokens.
        """
        # Refresh the tokens before adding the other list
        self._refresh()
        return super().__add__(other)

    def __iadd__(self, other: list[Token]) -> list[Token]:
        """
        Adds the other list of tokens to the list of tokens in place.

        Args:
            other (list[Token]): The other list of tokens.

        Returns:
            list[Token]: The combined list of tokens.
        """
        # Refresh the tokens before adding the other list
        self._refresh()
        return super().__iadd__(other)

    def __mul__(self, n: int) -> list[Token]:
        """
        Multiplies the list of tokens by the given number.

        Args:
            n (int): The number to multiply the list by.

        Returns:
            list[Token]: The multiplied list of tokens.
        """
        # Refresh the tokens before multiplying the list
        self._refresh()
        return super().__mul__(n)

    def __imul__(self, n: int) -> list[Token]:
        """
        Multiplies the list of tokens by the given number in place.

        Args:
            n (int): The number to multiply the list by.

        Returns:
            list[Token]: The multiplied list of tokens.
        """
        # Refresh the tokens before multiplying the list
        self._refresh()
        return super().__imul__(n)

    def __rmul__(self, n: int) -> list[Token]:
        """
        Multiplies the list of tokens by the given number.

        Args:
            n (int): The number to multiply the list by.

        Returns:
            list[Token]: The multiplied list of tokens.
        """
        # Refresh the tokens before multiplying the list
        self._refresh()
        return super().__rmul__(n)
