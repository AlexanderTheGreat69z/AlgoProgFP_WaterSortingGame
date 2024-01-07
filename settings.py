import pygame
from colors import *
pygame.mixer.init()

# Game base Variables
WINDOW_SIZE         = (1080, 720)
BACKGROUND_COLOR    = (0, 0, 50)
START_SCENE         = 'main-menu'
BUTTON_SIZE         = (100, 50)

# Sounds
BACKGROUND_MUSIC    = pygame.mixer.Sound(r'Water Game (PyGame)/assets/game_music.mp3')
POUR_SFX            = pygame.mixer.Sound(r'Water Game (PyGame)/assets/pour.mp3')
GG_SFX              = pygame.mixer.Sound(r'Water Game (PyGame)/assets/yay.mp3')
RESET_SFX           = pygame.mixer.Sound(r'Water Game (PyGame)/assets/reset.mp3')
SELECT_SFX          = pygame.mixer.Sound(r'Water Game (PyGame)/assets/select.mp3')
DESELECT_SFX        = pygame.mixer.Sound(r'Water Game (PyGame)/assets/deselect.mp3')
NOPE_SFX            = pygame.mixer.Sound(r'Water Game (PyGame)/assets/nope.mp3')

# Gameplay Variables
INCREASE_THRESHOLD  = 5
DEFAULT_RESETS      = 3

# Container Variables
CONTAINER_SIZE      = (90, 400)
CONTAINER_NUM       = 6
CONTAINER_CAP       = 4
CONTAINER_COL       = [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA, GRAY, DARKGREEN, DARKMAGENTA, LIGHTMAGENTA, LIGHTBLUE]


# initial list color => [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA, GRAY, DARKGREEN, DARKMAGENTA, LIGHTMAGENTA, LIGHTBLUE]
