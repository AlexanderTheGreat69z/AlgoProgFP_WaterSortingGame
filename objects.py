import pygame
from settings import *
from colors import *

# Text
class Text:
    
    # Get string and size
    def __init__(self, text, size):
        self.font = pygame.font.SysFont('freesansbold.ttf', size)
        self.text = self.font.render(text, True, WHITE)
        
        # Get the rect
        self.rect = self.text.get_rect()
    
    # Draws text to surface
    def drawText(self, surface):
        surface.blit(self.text, self.rect)

# Buttons
class Button:
    def __init__(self, size = tuple, text = str):
        self.button_size    = size
        self.text_size      = int(sum(self.button_size) / 4)
        self.text           = Text(text, self.text_size)
        self.rect           = pygame.Rect(0, 0, *self.button_size)
        self.default_color  = BLUE
        self.hover_color    = LIGHTBLUE
    
    def drawButton(self, surface):
        # Mouse Attributes
        mouse = pygame.mouse.get_pos()
        
        # Button Text
        self.text.rect.center = self.rect.center
        
        # Draw Button
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.default_color, self.rect)
            
        self.text.drawText(surface)

# Water content in containers
class Water:
    def __init__(self, color):
        
        # Water Attributes
        self.width  = CONTAINER_SIZE[0]
        self.height = CONTAINER_SIZE[1] / CONTAINER_CAP
        self.rect   = pygame.Rect(0, 0, self.width, self.height)
        self.color  = color
    
    # Draw water to container
    def addWater(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Containers
class Container:
    def __init__(self):
        
        # Container Dimensions
        self.width, self.height = CONTAINER_SIZE
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.thickness = 5
        
        # Container Colors
        self.default_color = WHITE
        self.hover_color = DARKCYAN
        
        # Filled with Water objects
        self.content = []
    
    # draw container to game
    def drawContainer(self, scene):
        
        # Get mouse position
        mouse = pygame.mouse.get_pos()
        
        # Draw the water content in list
        for water in self.content:
            
            # Get the index of water object
            index = self.content.index(water)
            
            # Position water fill
            if index == 0: water.rect.bottom = self.rect.bottom
            else: water.rect.bottom = self.content[index - 1].rect.top
            water.rect.centerx = self.rect.centerx
            
            # Fill the water object to container
            water.addWater(scene.surface)
        
        # Draw the container (with hover detail)
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(scene.surface, self.hover_color, self.rect, self.thickness)
        else:
            pygame.draw.rect(scene.surface, self.default_color, self.rect, self.thickness)
    
    # Insert top color to another container
    def fill(self, color):
        if len(self.content) < CONTAINER_CAP:
            new_water = Water(color)
            self.content.append(new_water)
    
    # Pour color to the top of another container
    def pour(self):
        if len(self.content) > 0:
            del self.content[-1]