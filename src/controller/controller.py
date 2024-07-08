from src.game_build.minesweeper import ModeFactory, Mode
# todo : controller receives user input as mouse clicks
#   As a minesweeper controller
#   I want to record player interactions in the form of mouse clicks
#   So that I can understand the player's intended action on the board
class Controller:
    def __init__(self):
        self.mode_factory = ModeFactory()


# todo: scenario CLICKING ON A REVEALED TILE
#   Given the game is in play
#   And the player clicks on a revealed tile
#   When the controller receives the mouse click
#   Then the controller should ignore the click

# todo: scenario RIGHT CLICKING ON AN UNREVEALED TILE WITH NO FLAG
#   Given the game is in play
#   And the player clicks on an unrevealed tile
#   And the tile is not flagged
#   When the controller receives the mouse click
#   Then the controller should determine the clicked tile's location on the board.
#   And relay the instruction to reveal the tile to the model

# todo: scenario RIGHT CLICKING ON AN UNREVEALED TILE WITH FLAG
#   Given the game is in play
#   And the player clicks on an unrevealed tile
#   And the tile is flagged
#   When the controller receives the mouse click
#   Then the controller should ignore the click

# todo: scenario LEFT CLICKING ON AN UNREVEALED TILE WITH NO FLAG
#   Given the game is in play
#   And the player clicks on an unrevealed tile
#   And the tile is not flagged
#   When the controller receives the mouse click
#   Then the controller should determine the clicked tile's location on the board.
#   And relay the instruction to toggle a flag on the tile to the model

# todo: scenario LEFT CLICKING ON AN UNREVEALED TILE WITH FLAG
#   Given the game is in play
#   And the player clicks on an unrevealed tile
#   And the tile is flagged
#   When the controller receives the mouse click
#   Then the controller should determine the clicked tile's location on the board.
#   And relay the instruction to toggle a flag on the tile to the model

# todo: scenario CLICKING OUTSIDE GAME BOARD
#   Given the game is in play
#   And the player clicks on an off-grid area
#   When the controller receives the mouse click
#   Then the controller should ignore the click

# todo: controller translates mouse clicks into meaningful game logic
#   As a minesweeper controller
#   I want to translate mouse clicks into meaningful actions for the model
#   So that I can determine intentions i.e "flag vs reveal"

# todo: controller communicates user input with model
#   As a minesweeper controller
#   I want to relay user input to the model
#   So that the model can update the game state

# todo: controller retrieves information from model to update display
#   As a minesweeper controller
#   I want to capture the updated game state
#   So that the viewer can display the updated game state

# todo: scenario MODEL GAME STATE IS WIN
#   Given the game is not in play
#   And the game state is a win
#   When the controller receives the information
#   Then the controller should instruct the view to update the game display with the winning sequence

# todo: scenario MODEL GAME STATE IS LOSE
#   Given the game is not in play
#   And the game state is a loss
#   When the controller receives the information
#   Then the controller should instruct the view to update the game display with the loss sequence

# todo: allowing the player to select or configure a board of their choice
#   As a minesweeper controller
#   I want to allow and handle the selection of board difficulty
#   So that the player begin the game with a pre-defined board size and difficulty level,
#   without needing to configure custom settings

# todo: scenario PLAYER SELECTS A DEFAULT BOARD
#   Given the player selects a default/predefined board
#   When the controller receives the information
#   Then the controller should relay the indicated configuration to the model
#   And the controller should capture the game state
#   And the controller should update the view with a visual of the selected board
#   And the board should have the stipulated dimensions

# todo: scenario PLAYER SELECTS TO CUSTOMISE BOARD
#   Given the player selects to customise a board
#   When the controller receives the information
#   Then the controller should bring up the customisation window
#   And relay the indicated configuration to the model
#   And the controller should capture the game state
#   And the controller should update the view with a visual of selected board
#   And the board should have the stipulated dimensions





