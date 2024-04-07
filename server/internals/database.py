"""
Database module for the server
"""
# Standard Library Imports
from hashlib import sha256
from typing import List

# Third Party Imports
from passlib.context import CryptContext
from psycopg2 import connect
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
    _context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

    @property
    def users(self) -> List[User]:
        """
        Gets all users from the database.

        Returns:
            List[User]: A list of all users.
        """
        self._logger.info("Getting all users")

        # Get the cursor
        cursor: RealDictCursor = self._connection.cursor(cursor_factory=RealDictCursor)

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
            email: str = None,
            token: str = None
    ) -> User | None:
        """
        Gets a user from the database using one of the provided parameters.

        Args:
            userId (int): The ID of the user.
            uuid (str): The UUID of the user.
            email (str): The email of the user.
            token (str): The token of the user.
        """
        # Ensure that at least one parameter is provided
        if userId is None and uuid is None and email is None and token is None:
            raise ValueError("At least one parameter must be provided.")

        self._logger.info(f"Getting user with ID {userId}, UUID {uuid}, and email {email}, and token {token}")

        # Get the cursor
        cursor: RealDictCursor = self._connection.cursor(cursor_factory=RealDictCursor)

        # Get the user
        cursor.execute(
            """
            SELECT * FROM users
            WHERE id = %s OR uuid = %s OR email = %s OR access_token = %s
            """,
            (userId, uuid, email, token)
        )
        row: RealDictRow = cursor.fetchone()
        if row is None:
            return None

        return User(row, self._connection)

    def addUser(
            self,
            email: str,
            password: str,
            username: str
    ) -> User:
        """
        Adds a user to the database.

        Returns:
            User: The user object.
        """
        self._logger.info(f"Adding user with email {email} and username {username}")

        # Get the cursor
        cursor: RealDictCursor = self._connection.cursor(cursor_factory=RealDictCursor)

        # Hash the password
        password = self._context.hash(password)

        # Add the user
        cursor.execute(
            """
            INSERT INTO users (email, password, username, access_token)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            (email, password, username, sha256(email.encode() + username.encode()).hexdigest())
        )
        row: RealDictRow = cursor.fetchone()

        return User(row, self._connection)

    """
===============================================================================================================================================================
        Games
===============================================================================================================================================================
    """

    @property
    def games(self) -> List[Game]:
        """
        Gets all games from the database.

        Returns:
            List[Game]: A list of all games.
        """
        self._logger.info("Getting all games")

        # Get the cursor
        cursor: RealDictCursor = self._connection.cursor(cursor_factory=RealDictCursor)

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
        cursor: RealDictCursor = self._connection.cursor(cursor_factory=RealDictCursor)

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
