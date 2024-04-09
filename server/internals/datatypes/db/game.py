"""
Contains the game class.
"""

# Standard Library Imports

# Third Party Imports
from psycopg2.extensions import connection as Connection
from psycopg2.extras import RealDictRow

# Local Imports
from ._base import DbBase, BaseModel
from .user import User
from ...config import Config


class GameModel(BaseModel):
    """
    Model for the game.
    """
    key: str
    width: int
    height: int
    time: int | None


class Game(DbBase):
    """
    Represents a game in the database.
    """
    # Type Hints
    _key: str
    _width: int
    _height: int
    _time: int | None  # Time in MS

    # Non-data properties
    _config: Config
    _connection: Connection

    def __init__(
            self,
            row: RealDictRow,
            connection: Connection,
            config: Config
    ) -> None:
        """
        Initializes the Game object.

        Args:
            row (RealDictRow): The row from the database.
            connection (Connection): The connection to use for database operations.
        """
        # Set the connection
        self._connection = connection
        self._config = config

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
        return [User(row, self._connection, self._config) for row in self._getAssoc("users")]

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

    """
================================================================================================================================================================
        Misc Methods
================================================================================================================================================================
    """

    def toModel(self) -> GameModel:
        """
        Converts the game to a model.

        Returns:
            GameModel: The game model.
        """
        return GameModel(
            id=self.id,
            createdAt=self.createdAt,
            key=self.key,
            width=self.width,
            height=self.height,
            time=self.time
        )
