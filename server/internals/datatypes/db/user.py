"""
Contains the user class.
"""
# Standard Library Imports

# Third Party Imports
from passlib.context import CryptContext
from psycopg2.extensions import connection as Connection
from psycopg2.extras import RealDictRow, RealDictCursor

# Local Imports
from ._base import DbBase, BaseModel
from .tokens import Tokens
from ...config import Config


class UserModel(BaseModel):
    """
    Model for the user.
    """
    uuid: str
    email: str
    username: str
    accessLevel: int
    refreshToken: str
    oauthScopes: list[str]


class User(DbBase):
    """
    Application user.
    """
    # Type hints
    _uuid: str
    _email: str
    _password: str
    _username: str
    _accessLevel: int
    _refreshToken: str
    _oauthScopes: list[str]

    # Password hashing context
    _context: CryptContext = CryptContext(schemes=["pbkdf2_sha512"], deprecated="auto")

    def __init__(
            self,
            row: RealDictRow,
            connection: Connection,
            config: Config
    ) -> None:
        """
        Initializes the User object.

        Args:
            row (RealDictRow): The row from the database.
            connection (Connection): The connection to use for database operations.
        """
        # Set the connection
        self._connection = connection

        # Set the config
        self._config = config

        # Get the data from the row
        userId = row["id"]
        createdAt: str = row["created_at"]
        super().__init__("users", connection, userId, createdAt)

        # Set all other data
        self._uuid: str = row["uuid"]
        self._email: str = row["email"]
        self._password: str = row["password"]
        self._username: str = row["username"]
        self._accessLevel: int = row["access_level"]
        self._refreshToken: str = row["refresh_token"]
        self._oauthScopes: list[str] = row["oauth_scopes"]

    """
================================================================================================================================================================
        Properties
================================================================================================================================================================
    """

    @property
    def uuid(self) -> str:
        """
        The UUID of the user.

        Returns:
            str: The UUID of the user.
        """
        return self._uuid  # Do not define a setter for this property, as it must not be changed

    @property
    def email(self) -> str:
        """
        The email of the user.

        Returns:
            str: The email of the user.
        """
        return self._email

    @email.setter
    def email(
            self,
            email: str
    ) -> None:
        """
        Sets the email of the user.

        Args:
            email (str): The email to set.

        Returns:
            None
        """
        self._set("email", email)
        self._email = email

    @property
    def username(self) -> str:
        """
        The username of the user.

        Returns:
            str: The username of the user.
        """
        return self._username

    @username.setter
    def username(
            self,
            username: str
    ) -> None:
        """
        Sets the username of the user.

        Args:
            username (str): The username to set.

        Returns:
            None
        """
        self._set("username", username)
        self._username = username

    @property
    def password(self) -> str:
        """
        The password of the user.

        Returns:
            str: The password of the user.
        """
        raise AttributeError("The password cannot be accessed directly.")

    @password.setter
    def password(
            self,
            password: str
    ) -> None:
        """
        Sets the password of the user.

        Args:
            password (str): The password to set.

        Returns:
            None
        """
        # Hash the password
        hashed = self._context.hash(password)

        # Remove the old password from memory
        del password

        # Set the new password
        self._set("password", hashed)
        self._password = hashed

    @property
    def accessLevel(self) -> int:
        """
        The access level of the user.

        Returns:
            int: The access level of the user.
        """
        return self._accessLevel

    @accessLevel.setter
    def accessLevel(
            self,
            accessLevel: int
    ) -> None:
        """
        Sets the access level of the user.

        Args:
            accessLevel (int): The access level to set.

        Returns:
            None
        """
        self._set("access_level", accessLevel)
        self._accessLevel = accessLevel

    @property
    def banned(self) -> bool:
        """
        Whether the user is banned.

        Returns:
            bool: Whether the user is banned.
        """
        return self._accessLevel == -1

    @banned.setter
    def banned(
            self,
            banned: bool
    ) -> None:
        """
        Sets whether the user is banned.

        Args:
            banned (bool): Whether the user is banned.

        Returns:
            None
        """
        self._set("access_level", -1 if banned else 0)
        self._accessLevel = -1 if banned else 0

    @property
    def refreshToken(self) -> str:  # Do not define a setter for this property, as it must not be changed
        """
        The access token of the user.

        Returns:
            str: The access token of the user.
        """
        return self._refreshToken

    @property
    def accessTokens(self) -> Tokens:
        """
        The access tokens of the user.

        Returns:
            list[str]: The access tokens of the user.
        """
        # This is a special case, as it requires a database operation to get the tokens
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM tokens
                WHERE user_id = %s
                """,
                (self.id,)
            )
            rows: list[RealDictRow] = cursor.fetchall()
            return Tokens(
                rows,
                self._connection,
                self._config.tokenExpireTime,
                self._config.jwtSecret,
                self.id,
                self.email
            )

    @property
    def oauthScopes(self) -> list[str]:
        """
        The OAuth scopes of the user.

        Returns:
            list[str]: The OAuth scopes of the user.
        """
        return self._oauthScopes

    @oauthScopes.setter
    def oauthScopes(
            self,
            oauthScopes: list[str]
    ) -> None:
        """
        Sets the OAuth scopes of the user.

        Args:
            oauthScopes (list[str]): The OAuth scopes to set.

        Returns:
            None
        """
        self._set("oauth_scopes", oauthScopes)
        self._oauthScopes = oauthScopes

    """
================================================================================================================================================================
        Non-data-operation methods
================================================================================================================================================================
    """

    def dict(self) -> dict:
        """
        Returns the user as a dictionary. This is reimplemented here because the password should not be included.

        Returns:
            dict: The user as a dictionary.
        """
        return {
            "id": self.id,
            "createdAt": self.createdAt,
            "uuid": self.uuid,
            "email": self.email,
            "username": self.username,
            "accessLevel": self.accessLevel,
            "banned": self.banned,
            "refreshToken": self.refreshToken,
            "accessTokens": self.accessTokens,
            "oauthScopes": self.oauthScopes
        }

    def __str__(self) -> str:
        """
        Returns the string representation of the user.

        Returns:
            str: The string representation of the user.
        """
        return f"{self.username} ({self.email})"

    def __repr__(self) -> str:
        """
        Returns the string representation of the user.

        Returns:
            str: The string representation of the user.
        """
        return self.__str__()

    """
================================================================================================================================================================
        Miscellaneous
================================================================================================================================================================
    """

    def checkPassword(
            self,
            password: str
    ) -> bool:
        """
        Checks if the given password is correct.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return self._context.verify(password, self._password)

    def toModel(self) -> UserModel:
        """
        Converts the user to a model.

        Returns:
            UserModel: The user model.
        """
        return UserModel(
            id=self.id,
            createdAt=self.createdAt,
            uuid=self.uuid,
            email=self.email,
            username=self.username,
            accessLevel=self.accessLevel,
            refreshToken=self.refreshToken,
            oauthScopes=self.oauthScopes
        )
