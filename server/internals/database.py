"""
Database module for the server
"""

# Standard Library Imports
from typing import List

# Third Party Imports
from psycopg2 import connect, sql
from psycopg2.sql import SQL
from psycopg2.extensions import connection as Connection
from psycopg2.extras import RealDictCursor, RealDictRow

# Local Imports
from .config import Config
from .datatypes.db import User, Game
from .logging import SuppressedLoggerAdapter, createLogger


class Database:
    """
    Database module for the server.
    """
    # Type hints
    _logger: SuppressedLoggerAdapter
    _config: Config
    _connection: Connection

    def __init__(
            self,
            config: Config
    ) -> None:
        """
        Initializes the Database object.

        Args:
            config (Config): The configuration object.

        Returns:
            None
        """
        self._config = config
        self._connection = connect(
            dbname=config.dbName,
            user=config.dbUser,
            password=config.dbPassword,
            host=config.dbIp,
            port=config.dbPort
        )
        # Create the logger
        self._logger = createLogger(
            "Database",
            databaseConnection=self._connection
        )

    def __del__(self) -> None:
        """
        Closes the database connection.
        """
        self._connection.close()

    """
===============================================================================================================================================================
        Properties
===============================================================================================================================================================
    """

    @property
    def connection(self) -> Connection:
        """
        The connection to the database.

        Returns:
            Connection: The connection to the database.
        """
        return self._connection

    """
===============================================================================================================================================================
        Users
===============================================================================================================================================================
    """

    def users(self) -> List[User]:
        """
        Gets all users from the database.

        Returns:
            List[User]: A list of all users.
        """
        self._logger.info("Getting all users")

        # Get the cursor
        cursor = self._connection.cursor(cursor_factory=RealDictCursor)

        # Get the users
        cursor.execute(
            """
            SELECT * FROM users
            """
        )
        rows: List[RealDictRow] = cursor.fetchall()
        return [User(row, self._connection) for row in rows]

    def getUser(
            self,
            userId: int = None,
            uuid: str = None,
            email: str = None
    ) -> User | None:
        """
        Gets a user from the database using one of the provided parameters.

        Args:
            userId (int): The ID of the user.
            uuid (str): The UUID of the user.
            email (str): The email of the user.
        """
        # Ensure that at least one parameter is provided
        if userId is None and uuid is None and email is None:
            raise ValueError("At least one parameter must be provided.")

        self._logger.info(f"Getting user with ID {userId}, UUID {uuid}, and email {email}")

        # Get the cursor
        cursor = self._connection.cursor(cursor_factory=RealDictCursor)

        # Get the user
        cursor.execute(
            """
            SELECT * FROM users
            WHERE id = %s OR uuid = %s OR email = %s
            """,
            (userId, uuid, email)
        )
        row: RealDictRow = cursor.fetchone()
        if row is None:
            return None

        return User(row, self._connection)

    """
===============================================================================================================================================================
        Games
===============================================================================================================================================================
    """

    def games(self) -> List[Game]:
        """
        Gets all games from the database.

        Returns:
            List[Game]: A list of all games.
        """
        self._logger.info("Getting all games")

        # Get the cursor
        cursor = self._connection.cursor(cursor_factory=RealDictCursor)

        # Get the games
        cursor.execute(
            """
            SELECT * FROM games
            """
        )
        rows: List[RealDictRow] = cursor.fetchall()
        return [Game(row, self._connection) for row in rows]

    def getGame(
            self,
            gameId: int = None,
            uuid: str = None
    ) -> Game | None:
        """
        Gets a game from the database using one of the provided parameters.

        Args:
            gameId (int): The ID of the game.
            uuid (str): The UUID of the game.

        Returns:
            Game: The game object.
        """
        # Ensure that at least one parameter is provided
        if gameId is None and uuid is None:
            raise ValueError("At least one parameter must be provided.")

        self._logger.info(f"Getting game with ID {gameId} and UUID {uuid}")

        # Get the cursor
        cursor = self._connection.cursor(cursor_factory=RealDictCursor)

        # Get the game
        cursor.execute(
            """
            SELECT * FROM games
            WHERE id = %s OR uuid = %s
            """,
            (gameId, uuid)
        )
        row: RealDictRow = cursor.fetchone()
        if row is None:
            return None

        return Game(row, self._connection)
