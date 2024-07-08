from src.viewer import landing
from src.controller.controller import Controller
from src.viewer.view import View
import pygame

pygame.init()
# todo: THE GENERAL MVC STORY
#  mvc uses all codebase components to create a wonderful minesweeper experience
#   As an mvc
#   I want to manage interactions between the model (game_build), the view and the controller
#   So that I can ensure the game process runs smoothly for an overall good user experience

# todo: 1. THE INITIAL VIEW STORY
#  the mvc starts up view to facilitate landing page player navigation
#   I want to start up the view component
#   So that it can bring up the landing page
#   .
#   scenario: the landing screen is brought up
#   Given the application is running
#   When the view has been initialised
#   Then the landing page with preview, info, choose board should be displayed

# todo: 2 THE LANDING PAGE STORY
#  the mvc receives player input from the view via mouse clicks on the landing page
#   I want the view to handle player (mouse clicks) on the landing page and constituents
#   So that the view can display the requested page to the player as they navigate the landing
#   .
#   scenario: the player selects the help/info page
#   Given the landing page is up
#   And the player selects the help icon
#   When the mvc receives the mouse click
#   Then the viewer should bring up the help page
#   And the help page should show up
#   And it should display information about the logic of the game
#   And it should have a preview button (eye)
#   And it should have a back/home button
#   And the home button should be a logo of a house
#   .
#   scenario: the player selects the back/home button from help/info page
#   Given the landing page is up
#   And the player selects the home icon
#   When the mvc receives the mouse click
#   Then the viewer should bring up the landing page again
#   And the landing page should be be displayed
#   And it should look as usual
#   .
#   scenario: the player selects the preview icon from landing page
#   Given the landing page is up
#   And the player selects the preview icon
#   When the mvc receives the mouse click
#   Then the viewer should bring up the preview page
#   And it should have clips/gifs of game state screenshots
#   And it should have a home icon
#   And it should have a help icon
#   .
#   scenario: the player selects the choose board button from the landing page
#   Given the landing page is up
#   And the player selects the choose board button
#   When the mvc receives this mouse click
#   Then the viewer should bring up the board selection page
#   And it should display all preset difficulties and configurations
#   And it should include a customise board button
#   .
#   scenario: the player selects a default board from the choose board page
#   Given that the choose board page is up
#   And the player selects a default board configuration
#   When the mvc receives this mouse click
#   Then the Board instance should be initialised using the selection
#   And the Game instance should be initialised using the board
#   And the controller should be set up to record the game state
#   And the controller should instruct the view to display the game state
#   And the game screen should be displayed
#   And all tiles of the board should be unrevealed
#   And the screen should contain a grid, 00:00 frozen timer, flag count, switch board, restart, home
#   And the grid should reflect the selected configuration size and flags allowed/mines on grid respectively
#   .
#  TODO 3: THE CONTROLLER STORY
#   As an mvc
#   I want to start up the controller relay info to and from the model and view
#   So that i can manage the game flow
#   .
#   scenario: the player makes a first move
#   Given game is in play
#   And the player right clicks a tile on the grid
#   When the mvc receives this mouse click
#   Then controller should determine the board location and intention of the mouse click
#   And the model should update the game state by revealing the selected tile
#   And the controller should record the game state
#   And the controller should instruct the view to display the game state
#   And the game screen should be updated with at least 9 revealed tiles depending on the difficulty
#   And the screen should contain a grid, timer, flag count, switch board, restart, home
#   And the timer should be counting up the duration of game play in mm:ss format
#   And the grid should reflect be the selected configuration size and flags allowed/mines on grid respectively
#   .
#   scenario: the player flags a tile mid game play
#   Given game is in play
#   And the player has 2 flags remaining
#   And the player left clicks a tile on the grid
#   When the mvc receives this mouse click
#   Then controller should determine the board location and intention of the mouse click
#   And the controller must instruct the model to update the game state by flagging the selected tile
#   And the controller should record the game state
#   And the controller should instruct the view to display the game state
#   And the game screen should be updated with an additional flag icon at the selected location
#   And the screen should contain a grid, timer, flag count, switch board, restart, home
#   And the player should have one flag remaining
#   And the timer should be counting up the duration of game play in mm:ss format
#   And the grid should reflect the selected configuration size and flags allowed/mines on grid respectively
#   .
#   scenario: the player flags a tile pre game play
#   Given game is not in play
#   And the player left clicks a tile on the grid
#   When the mvc receives this mouse click
#   Then controller should ignore this click
#   And the view should remain as is
#  TODO 4: THE SPECIAL EVENTS STORY
#   As an mvc
#   I want The controller to instruct the view to provide special effects for wins/losses
#   So that it can be more interactive
#   .
#   scenario: the player has won
#   Given game is not in play
#   And the player left clicks a tile on the grid
#   When the mvc receives this mouse click
#   Then controller should ignore this click
#   And the view should remain as is


def model_view_controller():
    view = View()
    control = Controller()




if __name__ == "__main__":
    landing.main()
