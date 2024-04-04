"""
Main file for the project
"""

# Standard Library Imports

# Third Party Imports
from fastapi import FastAPI

# Local Imports
from internals import Config, Database
from internals.datatypes.db import User, Game
from internals.logging import createLogger, SuppressedLoggerAdapter

# Create the FastAPI app
app: FastAPI = FastAPI()

# Create the internals objects
config: Config = Config()
database: Database = Database(config)
logger: SuppressedLoggerAdapter = createLogger("Main", databaseConnection=database.connection)


# Create the routes
@app.get("/")
async def root() -> dict[str, str]:
    """
    The root route.

    Returns:
        dict[str, str]: The message.
    """
    # Test the database
    user: User = database.getUser(1)
    game: Game = database.getGame(1)

    return {"message": "Hello World"}
