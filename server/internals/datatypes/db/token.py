"""
Contains the token class.
"""
# Standard Library Imports
from datetime import datetime

# Third Party Imports
from psycopg2.extensions import connection as Connection
from psycopg2.extras import RealDictRow

# Local Imports
from ._base import DbBase


class Token(DbBase):
    """
    Represents a token in the database.
    """
    # Type hints
    _token: str
    _expiration: datetime

    def __init__(
            self,
            row: RealDictRow,
            connection: Connection
    ) -> None:
        """
        Initializes the Token object.

        Args:
            row (RealDictRow): The row from the database.
            connection (Connection): The connection to use for database operations.
        """
        # Set the connection
        self._connection = connection

        # Get the data from the row
        tokenId = row['id']
        createdAt: str = row['created_at']
        super().__init__("tokens", connection, tokenId, createdAt)

        # Set all other data
        self._token = row['token']
        self._expiration = row['expiration']

    """
================================================================================================================================================================
        Properties
        
        Note: 
        - The expiration property is a special case. It is a datetime object. This is because the expiration time 
            is stored as a datetime object in the database. 
================================================================================================================================================================
    """

    @property
    def token(self) -> str:
        """
        Returns the token.

        Returns:
            str: The token.
        """
        return self._token

    @property
    def expiration(self) -> datetime:
        """
        Returns the expiration time.

        Returns:
            datetime: The expiration time.
        """
        return self._expiration
