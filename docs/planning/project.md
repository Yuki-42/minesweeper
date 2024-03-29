# Minesweeper Game

## Initial Idea

The initial idea for this project is for a competitive, socket-based minesweeper game where players compete to clear 
the board first.

The game parameters will be set by the host player (board size, mine probability). 

### Implementation

The game will be implemented using a server-client architecture where the server will be responsible for managing all 
game logic and the clients will be responsible for displaying and interacting with the game board.

The server will be implemented using Flask for the REST API and Flask-SocketIO for the websocket communication. The 
client will be implemented using plain HTML, CSS, and JavaScript using Vue.js.

The game will have a maximum game board size of 1024x1024 and a maximum mine probability of 0.5. Upon a new game creation,
the server will generate a new game board using the provided and store it in the database along with the game 
parameters and a game ID that is linked to the users that are playing the game. The server will not send the whole 
game board to the client, but rather the game state (revealed cells, flagged cells, etc.) and the client will render
the game board based on the game state. This is to prevent cheating by inspecting the game board in the browser.

The game will have no time limit, but the server will keep track of the time it took for each player to clear the board.

Upon game completion, the server will send a message to all clients stating the winner and the time it took for the
winner to clear the board. The clients will then have the option to start a new game. The server will store game statistics
in the database for future reference. These statistics will include the game ID, the players that participated, the winner,
the time it took for the winner to clear the board, and the game parameters. The server will not store the game board
itself, as it can be regenerated using the game parameters.

The game board will system will work on the server side as follows:
- The server will generate a binary matrix of size `board_size` x `board_size` where each cell has a probability `mine_probability` of being a mine.
- The server will then calculate the number of mines adjacent to each cell and store this information in a separate matrix.
- The server will then convert the binary matrix into a hexadecimal string and store it in the database. This is the board key that allows the server to regenerate the game board.
- The server will store the game state in a [dictionary](#game-state-handling).

### Game State Handling

The game state will be stored in a server-side [dictionary](#game-state-dict) where the keys are the game IDs and the 
values are LiveGame objects.

#### Game state dict

The game state will have the following structure:

```python
{
    gameId: LiveGame
}
```

#### Game Object

The Game object is a class used both as a parent class for the LiveGame object and as a way to represent the game in 
the database. The structure of the Game object will not be covered here.

#### LiveGame Object

The LiveGame object will have the following additional attributes compared to the Game object:
- `boards`: A dictionary containing the player IDs as keys and [Board](#board-object) objects as values.

#### Board Object

The Board object will have the following attributes:
- `board`: A list of [Cell](#cell-object) objects representing the game board. The list is flattened, so the index of a cell can be calculated as `row * board_size + col`.

#### Cell Object

The Cell object will have the following attributes:
- `mine`: A boolean indicating whether the cell is a mine.
- `adjacentMines`: An integer indicating the number of mines adjacent to the cell.
- `revealed`: A boolean indicating whether the cell has been revealed.
- `flagged`: A boolean indicating whether the cell has been flagged.

