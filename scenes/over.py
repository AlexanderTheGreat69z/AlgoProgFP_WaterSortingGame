import pygame, sys
from colors import *
from settings import INCREASE_THRESHOLD, DEFAULT_RESETS
from objects import Text, Button

# Game Over scene
class GameOver:
    def __init__(self, main):
        
        # Scene Attributes
        self.main = main
        self.surface        = main.window
        self.gsm            = main.gsm
        self.surf_rect      = self.surface.get_rect()
        self.bg_color       = DARKGREEN
        
        self.level          = 1
        self.threshold      = INCREASE_THRESHOLD
        
        # Title text
        self.title = Text("GGWP!", 100)
        self.title.rect.center = self.surf_rect.center
        
        # Play Button
        self.play = Button((100, 50), 'NEXT')
        self.play.rect.centerx = self.surf_rect.centerx
        self.play.rect.top = self.title.rect.bottom + 50
        
        # Quit Button
        self.quit = Button((100, 50), 'QUIT')
        self.quit.rect.centerx = self.surf_rect.centerx
        self.quit.rect.top = self.play.rect.bottom + 25
    
    # Draw the record of moves done in that level
    def _drawMovesRecord(self):
        
        # Instantiate text
        game = self.main.states['game-play']
        text = f'Sorted in {game.moves} moves with {DEFAULT_RESETS - game.resets} resets'
        draw = Text(text, 32)
        
        # Align text
        draw.rect.centerx = self.surf_rect.centerx
        draw.rect.top = self.title.rect.bottom
        
        # Draw text
        draw.drawText(self.surface)
        
    # Event handlers
    def _event(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                
                # Get cursor position and LMB click
                cursor = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()[0]
                
                # On play button click
                if self.play.rect.collidepoint(cursor) and click:
                    
                    # Game difficulty increases for every multiples of the threshold
                    if self.level % self.threshold == 0:
                        self.main.states['game-play'].increaseDifficulty()
                    
                    # Regenerate game stats for a new level
                    self.main.states['game-play'].regenerate()
                    
                    # Go to the game scene
                    self.gsm.setState('game-play')
                    
                    # Increase Level
                    self.level += 1
                
                # On quit button click
                if self.quit.rect.collidepoint(cursor) and click:
                    
                    # Quit the game (Stop program)
                    pygame.quit()
                    sys.exit()
    
    # Draws / Updates
    def _update(self):
        
        # Draw Background
        self.surface.fill(self.bg_color)
        
        # Draw GGWP text
        self.title.drawText(self.surface)
        
        # Draw moves record
        self._drawMovesRecord()
        
        # Draw buttons
        self.play.drawButton(self.surface)
        self.quit.drawButton(self.surface)
        
    # Scene execution
    def run(self):
        self._event()
        self._update()