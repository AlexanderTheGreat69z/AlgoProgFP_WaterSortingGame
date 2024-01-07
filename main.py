# Import Pygame along with settings
import pygame
from settings import WINDOW_SIZE, START_SCENE

# Import Game scenes
from scenes.game import WaterGame
from scenes.menu import MainMenu
from scenes.over import GameOver
pygame.init()

# Game State Manager to control scene transitions (basicly a class with a setter and getter)
class GSM:
    def __init__(self, current) : self.current = current
    def setState(self, state)   : self.current = state
    def getState(self)          : return self.current

# Main driver module
class main:
    def __init__(self):
        
        # Set game attributes
        self.window  = pygame.display.set_mode(WINDOW_SIZE)
        self.caption = pygame.display.set_caption("Sorting Bo'ols of Wo'ah")
        self.gsm     = GSM(START_SCENE)
        
        # Initialize Game Scenes
        self.states = {
            'main-menu' : MainMenu(self),
            'game-play' : WaterGame(self),
            'game-over' : GameOver(self),
        }
    
# Makes sure that this file is a script to run
if __name__ == "__main__":
    
    # Starts the program
    main = main()
    while True:
        main.states[main.gsm.getState()].run()
        pygame.display.update()