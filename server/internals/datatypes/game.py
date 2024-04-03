"""
Game data type
"""

# Local Imports
from .board import Board
from server.internals.datatypes.db.user import User


class Game:
    """
    Represents a game instance. Contains users and associated boards.
    """
    # Type hints
    boardKey: str
    boardWidth: int
    boardHeight: int
    mineProbability: float
    time
    users: list[User]
    boards: list[Board]

    def __init__(
            self,
            id: int,
            users: list[User],
            boards: list[Board]
    ) -> None:
        """
        Initializes the Game object.

        Args:
            id (int): The ID of the game.
            users (list[User]): The users in the game.
            boards (list[Board]): The boards in the game.

        Returns:
            None
        """
        self.id = id
        self.users = users
        self.boards = boards