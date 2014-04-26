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

#~ if __name__ == "__main__":
    #~ MainWindow = PyManMain()
    #~ MainWindow.MainLoop()
    
    
#~ import sys, pygame
#~ pygame.init()
#~ 
#~ size = (1100, 900)
#~ background_color = (127,255,212)
#~ screen = pygame.display.set_mode(size)
#~ board_area_x_offset = 300
#~ board_area_y_offset = 100
#~ board_area = screen.subsurface(Rect(board_area_x_offset,board_area_y_offset,700,700))
#~ 
#~ tile1 = pygame.image.load(os.path.join('images','tile-ttff-100px.png'))
#~ tile2 = pygame.image.load(os.path.join('images','tile-ttff-100px.png'))
#~ tile3 = pygame.image.load(os.path.join('images','tile-ttff-100px.png'))
#~ 
#~ ghost = pygame.image.load(os.path.join('images','item-ghost-100px.png'))
#~ 
#~ tile1rect = Rect(0,0,100,100)
#~ tile2rect = Rect(100,0,100,100)
#~ tile3rect = Rect(200,0,100,100)
#~ tile4rect = Rect(300,0,100,100)
#~ tile5rect = Rect(400,0,100,100)
#~ tile6rect = Rect(500,0,100,100)
#~ tile7rect = Rect(600,0,100,100)
#~ 
#~ tile1_rotation = 0
#~ tile2_rotation = 0
#~ tile3_rotation = 0
#~ 
#~ while 1:
    #~ for event in pygame.event.get():
        #~ if event.type == pygame.QUIT:
            #~ sys.exit()
        #~ if event.type == MOUSEBUTTONDOWN:
            #~ if event.button == 1:
                #~ mouse_x, mouse_y = event.pos
                #~ print mouse_x, mouse_y
                #~ 
                #~ #TODO implement func for this
                #~ if tile1rect.collidepoint((mouse_x-board_area_x_offset, mouse_y-board_area_y_offset)):
                    #~ print "collide 1"
                    #~ tile1_rotation += 90
                #~ if tile2rect.collidepoint((mouse_x-board_area_x_offset, mouse_y-board_area_y_offset)):
                    #~ print "collide 2"
                    #~ tile2_rotation += 90
                #~ if tile3rect.collidepoint((mouse_x-board_area_x_offset, mouse_y-board_area_y_offset)):
                    #~ print "collide 3"
                    #~ tile3_rotation += 90
                #~ 
        #~ screen.fill(background_color)
        #~ board_area.blit(pygame.transform.rotate(tile1,tile1_rotation), tile1rect)
        #~ board_area.blit(ghost, tile1rect)
        #~ board_area.blit(pygame.transform.rotate(tile2,tile2_rotation), tile2rect)
        #~ board_area.blit(pygame.transform.rotate(tile3,tile3_rotation), tile3rect)
        #~ board_area.blit(pygame.transform.rotate(tile3,tile3_rotation), tile4rect)
        #~ board_area.blit(pygame.transform.rotate(tile3,tile3_rotation), tile5rect)
        #~ board_area.blit(pygame.transform.rotate(tile3,tile3_rotation), tile6rect)
        #~ board_area.blit(pygame.transform.rotate(tile3,tile3_rotation), tile7rect)
        #~ 
        #~ pygame.display.flip()
        
        
#~ import os
#~ import pygame
#~ from pygame.locals import *
#~ 
#~ pygame.init()
#~ screen = pygame.display.set_mode((500, 500), HWSURFACE | DOUBLEBUF | RESIZABLE)
#~ pic = pygame.image.load(os.path.join('images','tile-ttff-100px.png'))
#~ screen.blit(pygame.transform.scale(pic, (500, 500)), (0, 0))
#~ pygame.display.flip()
#~ while True:
    #~ pygame.event.pump()
    #~ event = pygame.event.wait()
    #~ if event.type == QUIT:
        #~ pygame.display.quit()
    #~ elif event.type == VIDEORESIZE:
        #~ screen = pygame.display.set_mode(
            #~ event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
        #~ screen.blit(pygame.transform.scale(pic, event.dict['size']), (0, 0))
        #~ pygame.display.flip()
        
