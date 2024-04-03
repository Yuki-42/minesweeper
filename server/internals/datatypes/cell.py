"""
Cell datatype. Represents a cell in the game board.
"""


class Cell:
    """
    Represents a singular cell in the game board.
    """
    # Type hints
    mine: bool
    adjacentMines: int
    revealed: bool
    flagged: bool

    def __init__(
            self,
            mine: bool,
            adjacentMines: int,
            revealed: bool = False,
            flagged: bool = False
    ) -> None:
        """
        Initializes the Cell object.

        Args:
            mine (bool): Whether the cell contains a mine.
            adjacentMines (int): The number of mines adjacent to the cell.
            revealed (bool): Whether the cell has been revealed.
            flagged (bool): Whether the cell has been flagged.

        Returns:
            None
        """
        self.mine = mine
        self.adjacentMines = adjacentMines
        self.revealed = revealed
        self.flagged = flagged
