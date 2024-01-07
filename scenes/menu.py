import pygame
from settings import BACKGROUND_COLOR, BACKGROUND_MUSIC
from colors import *
from objects import Text, Button

# Menu scene
class MainMenu:
    def __init__(self, main):
        
        # Scene Attributes
        self.surface        = main.window
        self.gsm            = main.gsm
        self.surf_rect      = self.surface.get_rect()
        self.bg_color       = BACKGROUND_COLOR
        self.bgm            = BACKGROUND_MUSIC
        
        # Title text
        self.title = Text("SORTING WO'AH BO'OLS", 100)
        self.title.rect.center = self.surf_rect.center
        
        # Play Button
        self.play = Button((100, 50), 'PLAY')
        self.play.rect.centerx = self.surf_rect.centerx
        self.play.rect.top = self.title.rect.bottom + 50
        
        # Quit Button
        self.quit = Button((100, 50), 'QUIT')
        self.quit.rect.centerx = self.surf_rect.centerx
        self.quit.rect.top = self.play.rect.bottom + 25
        
    # Game event handling
    def _event(self):
        for e in pygame.event.get():
            
            # On window exit, quit game
            if e.type == pygame.QUIT: pygame.quit()
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                
                # Get cursor position and LMB click
                cursor = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()[0]
                
                # On play button click, go to game
                if self.play.rect.collidepoint(cursor) and click:
                    self.bgm.play(-1)
                    self.gsm.setState('game-play')
                
                # On quit button click, quit game
                if self.quit.rect.collidepoint(cursor) and click: pygame.quit()
    
    # Game draws/updates
    def _update(self):
        
        # Draw bAckground
        self.surface.fill(self.bg_color)
        
        # Draw game title
        self.title.drawText(self.surface)
        
        # Draw buttons
        self.play.drawButton(self.surface)
        self.quit.drawButton(self.surface)
        
    # Scene execution
    def run(self):
        self._event()
        self._update()
        