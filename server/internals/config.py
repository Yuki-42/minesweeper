"""
The config module.
"""

# Standard Library Imports
from os import environ

# Third Party Imports
from dotenv import load_dotenv as loadDotEnv


class Config:
    """
    Configuration class for the server.
    """
    # Type hints
    dbIp: str
    dbPort: str
    dbName: str
    dbUser: str
    dbPassword: str

    def __init__(self) -> None:
        """
        Initializes the Config object.

        Returns:
            None
        """
        # Load the environment variables
        loadDotEnv()

        # Set the database variables
        self.dbIp = environ.get("DB_IP")
        self.dbPort = environ.get("DB_PORT")
        self.dbName = environ.get("DB_NAME")
        self.dbUser = environ.get("DB_USER")
        self.dbPassword = environ.get("DB_PASS")
