"""
Board data type.
"""
# Standard Library Imports
from random import random

# Local Imports
from .cell import Cell


# Helper functions
def decision(
        probability: float
) -> bool:
    """
    Returns True with a probability of probability.

    Args:
        probability (float): The probability of returning True.

    Returns:
        bool: True with a probability of probability.
    """
    return random() < probability


def countAdjacent(
        cellBinary: list[bool],
        width: int,
        index: int
) -> int:
    """
    Returns the number of mines adjacent to the cell at index.

    Args:
        cellBinary (list[bool]): The list of cells.
        width (int): The width of the board.
        index (int): The index of the cell.

    Returns:
        int: The number of mines adjacent to the cell at index.
    """
    # Subtract 1 from the width to account for 0-based indexing
    # width -= 1

    # Pre-declare count and fetch index
    count: int = 0

    # Ensure that the index is within the bounds of the list
    if index < 0 or index >= len(cellBinary):
        raise ValueError("Index out of bounds")

    # Ensure that the list forms any kind of rectangle
    if len(cellBinary) % width != 0:
        raise ValueError("List does not form a rectangle")

    # Create list of indices to check. This should be a list of indices that are adjacent to the cell

    # TODO: Refactor this code to generate all indices and then remove the invalid ones

    # Logic for corner cases
    if index == 0:  # Top left
        fetchIndex = [
            1,  # Right
            width,  # Bottom
            width + 1  # Bottom right
        ]
    elif index == width - 1:  # Top right
        fetchIndex = [
            width - 2,  # Left
            2 * width - 1,  # Bottom
            2 * width - 2  # Bottom left
        ]
    elif index == width * (width - 1):  # Bottom left
        fetchIndex = [
            width * (width - 2),  # Top
            width * (width - 1) + 1,  # Right
            width * (width - 2) + 1  # Top right
        ]
    elif index == width ** 2 - 1:  # Bottom right
        fetchIndex = [
            width ** 2 - 2,  # Left
            width ** 2 - width - 1,  # Top
            width ** 2 - width - 2  # Top left
        ]

    # Logic for edge cases
    elif index < width:  # Top edge
        fetchIndex = [
            index - 1,  # Left
            index + 1,  # Right
            index + width,  # Bottom
            index + width - 1,  # Bottom left
            index + width + 1  # Bottom right
        ]
    elif index % width == 0:  # Left edge
        fetchIndex = [
            index - width,  # Top
            index - width + 1,  # Top right
            index + 1,  # Right
            index + width,  # Bottom
            index + width + 1  # Bottom right
        ]
    elif index % width == width - 1:  # Right edge
        fetchIndex = [
            index - width,  # Top
            index - width - 1,  # Top left
            index - 1,  # Left
            index + width,  # Bottom
            index + width - 1  # Bottom left
        ]
    elif index > width * (width - 1):  # Bottom edge
        fetchIndex = [
            index - 1,  # Left
            index + 1,  # Right
            index - width,  # Top
            index - width - 1,  # Top left
            index - width + 1  # Top right
        ]
    else:
        fetchIndex = [
            index - 1,  # Left
            index + 1,  # Right
            index - width,  # Top
            index + width,  # Bottom
            index - width - 1,  # Top left
            index - width + 1,  # Top right
            index + width - 1,  # Bottom left
            index + width + 1  # Bottom right
        ]

    # Throw an error if there are any negative indices
    if any(i < 0 for i in fetchIndex):
        raise ValueError("Negative index found")

    # Throw an error if there are any indices greater than the length of the list
    if any(i >= len(cellBinary) for i in fetchIndex):
        raise ValueError("Index out of bounds")

    # Throw an error if there are any duplicate indices
    if len(fetchIndex) != len(set(fetchIndex)):
        raise ValueError("Duplicate indices found")

    # Order the list of indices
    fetchIndex.sort()

    # Count the number of mines adjacent to the cell
    for i in fetchIndex:
        if cellBinary[i]:
            count += 1

    return count


def _verifyKey(
        key: str,
        cellCount: int
) -> str:
    """
    Verifies that the key is intact (this is very rare), if not corrects it.

    Args:
        key (str): The key to verify.
        cellCount (int): The number of cells in the board.

    Returns:
        str: The verified key.
    """
    # Ensure that the key is the correct length, if not, pad with zeroes
    if len(key) < cellCount // 4:
        key = "0" * (cellCount // 4 - len(key)) + key

    return key


class Board:
    """
    Represents a board instance. Contains cells.
    """
    # Type hints
    boardKey: str
    boardBits: str
    width: int
    height: int
    cells: list[Cell]
    probability: float

    def __init__(
            self,
            probability: float,
            width: int,
            height: int,
            boardKey: str = None
    ) -> None:
        """
        Initializes the Board object.

        Args:
            probability (float): The probability of a cell containing a mine.
            width (int): The width of the board.
            height (int): The height of the board.

        Returns:
            None
        """
        self.width = width
        self.height = height
        self.probability = probability

        # If a board key is not provided generate the board
        if boardKey is None:
            self._gen()
            return

        # Convert the hexadecimal key to binary
        self.boardKey = boardKey
        self.boardBits = bin(int(boardKey, 16))[2:]

        # Ensure that the board key is the correct length, if not, pad with zeroes
        if len(self.boardBits) < (width * height):
            self.boardBits = "0" * ((width * height) - len(self.boardBits)) + self.boardBits

        # Converse to list of boolean values representing whether a cell contains a mine
        cellBinary: list[bool] = [self.boardBits[i] == "1" for i in range(width * height)]

        # Generate the list of cells
        self.cells = [Cell(self.boardBits[i] == "1", countAdjacent(cellBinary, self.width, i)) for i in range(width * height)]

    def _gen(self) -> None:
        """
        Generates the board.

        Returns:
            None
        """
        # Precalculate the number of cells as it is used multiple times
        numCells: int = self.width * self.height

        # Generate list of boolean values representing whether a cell contains a mine
        cellBinary: list[bool] = [decision(self.probability) for _ in range(numCells)]

        # Generate list of Cell objects
        self.cells = [Cell(cellBinary[i], countAdjacent(cellBinary, self.width, i)) for i in range(numCells)]

        # Create binary string representation of the board
        self.boardBits = "".join("1" if cellBinary[i] else "0" for i in range(numCells))

        # Convert to hexadecimal
        self.boardKey = hex(int(self.boardBits, 2))[2:]

        # Verify that the key is intact
        self.boardKey = _verifyKey(self.boardKey, numCells)

    """
================================================================================================================================================================
        Overrides
================================================================================================================================================================
    """

    def __getitem__(  # This was a good idea copilot :)
            self,
            index: int
    ) -> Cell:
        """
        Returns the cell at index.

        Args:
            index (int): The index of the cell.

        Returns:
            Cell: The cell at index.
        """
        return self.cells[index]

    def __str__(self) -> str:
        """
        Returns a string representation of the board.

        Returns:
            str: A string representation of the board.
        """
        return f"{self.width}*{self.height}:{self.boardKey}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the board.

        Returns:
            str: A string representation of the board.
        """
        return f"Board({self.probability}, {self.width}, {self.height}, \"{self.boardKey}\")"
