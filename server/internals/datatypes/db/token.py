"""
Contains the token class.
"""
# Standard Library Imports
from datetime import datetime

# Third Party Imports
from psycopg2.extensions import connection as Connection
from psycopg2.extras import RealDictRow

# Local Imports
from ._base import DbBase, BaseModel


class TokenModel(BaseModel):
    """
    Model for the token.
    """
    userId: int
    token: str
    expiration: datetime


class Token(DbBase):
    """
    Represents a token in the database.
    """
    # Type hints
    userId: int
    token: str
    expiration: datetime

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
        super().__init__(
            "tokens",
            connection,
            row["id"],
            row["created_at"]
        )

        # Set all other data
        self.userId = row["user_id"]
        self.token = row["token"]
        self.expiration = row["expires_at"]

    def toModel(self) -> TokenModel:
        """
        Converts the token to a model.

        Returns:
            TokenModel: The token model.
        """
        return TokenModel(
            id=self.id,
            createdAt=self.createdAt,
            userId=self.userId,
            token=self.token,
            expiration=self.expiration
        )
