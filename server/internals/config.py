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
    databaseIp: str
    databasePort: str
    databaseName: str
    databaseUser: str
    databasePassword: str

    def __init__(self) -> None:
        """
        Initializes the Config object.

        Returns:
            None
        """
        # Load the environment variables
        loadDotEnv()

        # Set the database variables
        self.databaseIp = environ.get("DATABASE_IP")
        self.databasePort = environ.get("DATABASE_PORT")
        self.databaseName = environ.get("DATABASE_NAME")
        self.databaseUser = environ.get("DATABASE_USER")
        self.databasePassword = environ.get("DATABASE_PASSWORD")
