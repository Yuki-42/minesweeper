"""
Contains the game class.
"""

# Standard Library Imports

# Third Party Imports
from psycopg2.extensions import connection as Connection
from psycopg2.extras import RealDictRow
from psycopg2.sql import SQL, Identifier

# Local Imports
from server.internals.datatypes.db._base import DbBase
from server.internals.datatypes.db.user import User


class Game(DbBase):
    """
    Represents a game in the database.
    """
    # Type Hints
    _key: str
    _width: int
    _height: int
    _time: int | None  # Time in MS

    def __init__(
            self,
            row: RealDictRow,
            connection: Connection
    ) -> None:
        """
        Initializes the Game object.

        Args:
            row (RealDictRow): The row from the database.
            connection (Connection): The connection to use for database operations.
        """
        # Set the connection
        self._connection = connection

        # Get the data from the row
        gameId = row['id']
        createdAt: str = row['created_at']
        super().__init__("games", connection, gameId, createdAt)

        # Set all other data
        self._key = row['board_key']
        self._width = row['board_width']
        self._height = row['board_height']
        self._time = row['time']

    """
================================================================================================================================================================
        Properties
        
        Note: 
        - The time property is a special case. It is a nullable integer. This is because the time can be null 
            in the database. 
        - The time property is the only property with a setter, as it is the only property that may 
            be changed. 
================================================================================================================================================================
    """
    @property
    def key(self) -> str:
        """
        Returns the key of the game.

        Returns:
            str: The key of the game.
        """
        return self._key

    @property
    def width(self) -> int:
        """
        Returns the width of the game.

        Returns:
            int: The width of the game.
        """
        return self._width

    @property
    def height(self) -> int:
        """
        Returns the height of the game.

        Returns:
            int: The height of the game.
        """
        return self._height

    @property
    def time(self) -> int | None:
        """
        Returns the time of the game.

        Returns:
            int | None: The time of the game.
        """
        return self._time

    @time.setter
    def time(
            self,
            time: int | None
    ) -> None:
        """
        Sets the time of the game.

        Args:
            time (int | None): The time to set.

        Returns:
            None
        """
        self._set("time", time)
        self._time = time

    @property
    def users(self) -> list[User]:
        """
        Returns the users in the game.

        Returns:
            list[User]: The users in the game.
        """
        return [User(row, self._connection) for row in self._getAssoc("users")]

    # Allow someone to add a user to the game
    @users.setter  # IDK if this will work or not
    def users(
            self,
            user: User
    ) -> None:
        """
        Adds a user to the game.

        Args:
            user (User): The user to add.

        Returns:
            None
        """
        self._addAssoc("users", user.id)
