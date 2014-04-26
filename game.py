import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=900,height=900):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode(
            (self.width, self.height))
        
    def MainLoop(self):
        """This is the Main Loop of the Game"""
        
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
        
class Tile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('tile-ttff-100px.png',-1)
            
    def LoadSprites(self):
        """Load the sprites that we need"""
        self.tile = Tile()
        self.tile_sprites = pygame.sprite.RenderPlain((self.tile))
        """Load All of our Sprites"""
        self.LoadSprites();
        self.snake_sprites.draw(self.screen)
        pygame.display.flip()
