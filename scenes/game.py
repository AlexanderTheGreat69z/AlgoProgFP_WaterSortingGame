import pygame
from settings import *
from colors import *
from random import randint
from copy import deepcopy
from objects import Container, Text
pygame.mixer.init()

# Game scene
class WaterGame:
    def __init__(self, main):
        
        # Scene Attributes
        self.surface        = main.window
        self.gsm            = main.gsm
        self.font_size      = 32
        self.surf_rect      = self.surface.get_rect()
        self.bg_color       = BACKGROUND_COLOR
        
        # Sound FX
        self.pour_sfx       = POUR_SFX
        self.ggwp_sfx       = GG_SFX
        self.reset_sfx      = RESET_SFX
        self.select_sfx     = SELECT_SFX
        self.deselect_sfx   = DESELECT_SFX
        self.nope_sfx       = NOPE_SFX
        
        # Game Containers
        self.avail_colors   = CONTAINER_COL
        self.containers     = CONTAINER_NUM
        self.capacity       = CONTAINER_CAP
        self.empty          = 2
        self.filled         = self.containers - self.empty
        self.selected       = ''
        
        # Alignment spaces of generated containers
        # (Window width - n-containers x container width) / (n-spaces) => n-spaces = n-containers - 1
        self.window_width    = WINDOW_SIZE[0]
        self.container_width = CONTAINER_SIZE[0]
        self.container_space = (self.window_width - self.containers * self.container_width) / (self.containers - 1)
        
        # Counters
        self.level  = 1
        self.moves  = 0
        self.resets = DEFAULT_RESETS
        
        # Selected colors and count instances
        # self.game_colors = {color: instances(int)}
        self.color_instances = {}
        for color in range(self.filled): self._selectColor()
        self.game_colors = list(self.color_instances.keys()) 
        
        # Set of containers
        self.container_set = [Container(), Container()]
        for container in range(self.filled): self._generateContainer()
        
        # Store initial game set for resetting
        self.starting_set = deepcopy(self.container_set)
        
        # just a prototype container (only used during prototype, not in-game)
        self.test_con = Container()
        
    # Randomly select colors and set initial instance
    def _selectColor(self):
        
        # Randomly select a color from the COLOR list
        limit = len(self.avail_colors) - 1
        rand_color =self.avail_colors[randint(0, limit)]
        
        # Checks if the color is new in the selected colors dictionary
        if rand_color not in self.color_instances.keys():
            self.color_instances[rand_color] = 0
        else: self._selectColor()
    
    # Fill starting containers and count instances
    def _initialFill(self, container, colors):
        
        # Randomly select a color from the selected colors list
        limit = len(self.color_instances) - 1
        rand_color = colors[randint(0, limit)]
        
        # Checks if the instances of the color has reached capacity
        if self.color_instances[rand_color] < self.capacity:
            container.fill(rand_color)
            self.color_instances[rand_color] += 1
        else: self._initialFill(container, colors)
    
    # Generate containers
    def _generateContainer(self):
        # Instantiate new Container object
        container = Container()
        
        # Fill the container with colors from the selected colors list
        for color in range(self.capacity):
            self._initialFill(container, self.game_colors)
        
        # Append the object to the game set if it's not all equal
        if len(set(container.content)) != 1:
            self.container_set.append(container)
        else: self._generateContainer()
    
    # Generate a row of containers
    def _drawContainerRow(self):
        
        # Loops over containers in the list of containers
        for container in self.container_set:
            
            # Get the container index
            index = self.container_set.index(container)
            
            # 2nd container and so on follow the first container
            if index != 0:
                container.rect.left = self.container_set[index-1].rect.right + self.container_space
            container.rect.centery = self.surf_rect.centery
            container.drawContainer(self)
    
    # Reset game in case player is stuck
    def _resetGame(self):
        
        # Checks if there are available resets
        if self.resets > 0:
            
            # Clear game set
            self.container_set.clear()
            
            # Re-generate the initial game set
            for container in self.starting_set:
                self.container_set.append(container)
            
            # Secure initial game set
            self.starting_set = deepcopy(self.container_set)
            
            # Play sfx
            self.reset_sfx.play()
            
            # Decrease the number of resetc player can do
            self.resets -= 1
    
    # Container Selection
    def _selectContainer(self, cursor):
        # Scans every container in list of containers
        for container in self.container_set:
            
            # Checks if container is hovered and is not empty
            isHovered = container.rect.collidepoint(cursor)
            isNotEmpty = len(container.content) > 0
            if isHovered and isNotEmpty:
                
                # Updates the selected container on select
                if self.selected != '':
                    self.selected.default_color = WHITE
                    self.selected.default_color = WHITE
                self.selected = container
                
                # Set outline to selected container
                self.selected.default_color = GREEN
                self.selected.hover_color = GREEN
                
                # Play sfx when selected
                self.select_sfx.play()
        
    # Function to get multiple colors in a container for pouring
    def _multiPour(self, containerContent = list):
        
        # Get the top water of container 
        top_water = containerContent[-1]
        
        # Initiate a list of colors to be poured (starts with the first top color)
        sel_colors = [top_water.color]
        
        # Scan list elements from second last to first
        # If the element is equal to the last element (top of stack), append to list
        # Stop scan if not equal
        for index in range(-2, -len(containerContent)-1, -1):
            if containerContent[index].color == top_water.color:
                sel_colors.append(containerContent[index].color)
            else: break
        
        return sel_colors
        
    # Pour Selection
    def _pourWaters(self, cursor):
        
        # Scans every container in list of containers
        for container in self.container_set:
            
            # Checks if container is not the selected container and is hovered
            isNotSelected = container != self.selected
            isHovered = container.rect.collidepoint(cursor)
            if isNotSelected and isHovered:
                
                # Initiate a list of colors to be distributed
                poured_waters = self._multiPour(self.selected.content)
                
                # Checks if target container is empty or the top color of container is the same as top of selected
                if len(container.content) == 0 or container.content[-1].color == self.selected.content[-1].color:
                    
                    # Checks if the content of target container added with the colors is less than or equal to container cap
                    if len(container.content) + len(poured_waters) <= self.capacity:
                        
                        # Fill target container with the top color of selected container
                        for water in poured_waters:
                            container.fill(water)
                            self.selected.pour()
                            
                        # Add the number of moves
                        self.moves += 1
                        
                        # Play the pouring sfx
                        self.pour_sfx.play()
                    
                    else:
                        # Play sfx
                        self.nope_sfx.play()
                else:
                    # Play sfx
                    self.nope_sfx.play()
                    
                # Reset selected
                self.selected.default_color = WHITE
                self.selected = ''
                
            elif not isNotSelected and isHovered:
                
                # Reset selected
                self.selected.default_color = WHITE
                self.selected = ''
                
                # Play a deselect sfx
                self.deselect_sfx.play()
    
    # Check if all the colors of a container are equal
    def _checkColors(self, container):
        # Store the colors of a container in a list
        colors = []
        
        # Scans and appends color to list
        for water in container.content: colors.append(water.color)
        
        # Returns true if the colors in list are the same
        if len(set(colors)) == 1: return True
        else: return False
    
    # Checks all containers
    def _checkContainers(self):
        
        # Initiate check list
        checklist = []
        
        # Checks if the selecton is an int
        for container in self.container_set:
            
            # Is the container maxed out? (Content reached its capacity)
            containerMaxed = len(container.content) == self.capacity
            
            # Are all the colors in container the same?
            allSame = self._checkColors(container)
            
            # Is the container empty?
            isEmpty = len(container.content) == 0
            
            # If the the container is maxed and have same colors or is empty, make it valid
            if (containerMaxed and allSame) or isEmpty:
                checklist.append(True)
            else: checklist.append(False)
            
        # If there exists an invalid container in the checklist, return as invalid
        if False in checklist: return False
        else: return True
    
    # Draws level counter
    def _drawLevel(self):
        text = f'Level {self.level}'
        margin = 50
        
        counter = Text(text, self.font_size)
        counter.rect.centerx = self.surf_rect.centerx
        counter.rect.y += margin
        counter.drawText(self.surface)
    
    # Draw moves counter
    def _drawMove(self):
        text = f'Moves: {self.moves}'
        margin = 75
        
        counter = Text(text, self.font_size)
        counter.rect.centerx = self.surf_rect.centerx
        counter.rect.y += margin
        counter.drawText(self.surface)
    
    # Draws reset counter
    def _drawReset(self):
        text = f'Resets: {self.resets}'
        counter = Text(text, self.font_size)
        counter.rect.bottomleft = self.surf_rect.bottomleft
        counter.drawText(self.surface)
    
    # Key Press event
    def _keydown(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
            
            if e.key == pygame.K_SPACE:
                self._resetGame()
            
            # |Container Test| #
            # if e.key == pygame.K_1:
            #     self.test_con.fill(self.game_colors[0])
            # if e.key == pygame.K_2:
            #     self.test_con.fill(self.game_colors[1])
            # if e.key == pygame.K_3:
            #     self.test_con.fill(self.game_colors[2])
            # if e.key == pygame.K_4:
            #     self.test_con.fill(self.game_colors[3])
            # if e.key == pygame.K_SPACE:
            #     self.test_con.pour()
        
    # Mouse click event
    def _mouseclick(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            cursor = pygame.mouse.get_pos()
            if self.selected == '': self._selectContainer(cursor)
            else: self._pourWaters(cursor)
    
    # Events function
    def _event(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit()
            self._keydown(e)
            self._mouseclick(e)
    
    # Draws / Updates
    def _update(self):
        self.surface.fill(self.bg_color)
        self._drawLevel()
        self._drawMove()
        self._drawReset()
        self._drawContainerRow()
        
        # |Container Test| #
        # self.test_con.drawContainer(self)
        # print(self.color_instances)
    
    # Reset game stats and regenerate a new one
    def regenerate(self):
        
        # Increase level and reset moves and number of resets
        self.level += 1
        self.moves = 0
        self.resets = DEFAULT_RESETS
        
        # Re-generate new colors
        self.color_instances = {}
        for color in range(self.filled): self._selectColor()
        self.game_colors = list(self.color_instances.keys()) 
        
        # Re-generate game set
        self.container_set = [Container(), Container()]
        for container in range(self.filled): self._generateContainer()
        self.starting_set = deepcopy(self.container_set)
    
    # Increase difficulty of the level
    def increaseDifficulty(self):

        # If the num of containers are still below the maximum number of available colors, add the container by 1 to increase difficulty
        if self.containers < len(self.avail_colors):
            self.containers += 1
        
        # Update attributes relative to contianer number or game
        self.filled = self.containers - self.empty
        self.container_space = (WINDOW_SIZE[0] - self.containers * CONTAINER_SIZE[0]) / (self.containers - 1)
    
    # Scene execution
    def run(self):
        
        # Get completion check
        check = self._checkContainers()
        
        # Game runs as long as it's not complete. If it does, goes to game over scene
        if not check:
            self._event()
            self._update()
        else:
            wait_time = 1000 # Delay in miliseconds
            pygame.time.delay(wait_time)
            self.ggwp_sfx.play()
            self.gsm.setState('game-over')
        