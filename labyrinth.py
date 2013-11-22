# coding: utf8

import sys
import pygame
import os
from pygame.locals import *
from random import shuffle
from player import Player
from tile import BoardTile
from graph import Graph

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class NewGame:
    def __init__(self):
        """Setup the game"""
        
        # Misc Variables
        self.image_dir = 'images'
        
        # Board Grid (x right, y down)       
        self.board = { (0,0): None, (1,0): None, (2,0): None, (3,0): None, (4,0): None, (5,0): None, (6,0): None,
                       (0,1): None, (1,1): None, (2,1): None, (3,1): None, (4,1): None, (5,1): None, (6,1): None,
                       (0,2): None, (1,2): None, (2,2): None, (3,2): None, (4,2): None, (5,2): None, (6,2): None,
                       (0,3): None, (1,3): None, (2,3): None, (3,3): None, (4,3): None, (5,3): None, (6,3): None,
                       (0,4): None, (1,4): None, (2,4): None, (3,4): None, (4,4): None, (5,4): None, (6,4): None,
                       (0,5): None, (1,5): None, (2,5): None, (3,5): None, (4,5): None, (5,5): None, (6,5): None,
                       (0,6): None, (1,6): None, (2,6): None, (3,6): None, (4,6): None, (5,6): None, (6,6): None,}
        self.board_hash = {}
        
        # List of items in game
        self.items = ['genie', 'map', 'book', 'bat', 'skull', 'ring', 'sword',
                      'candles', 'gem', 'lizzard', 'spider', 'purse', 'chest',
                      'beetle', 'owl', 'keys', 'dwarf', 'helmet', 'fairy',
                      'moth', 'dragon', 'mouse', 'ghost', 'crown']
        self.actions = ['second_push', 'two_turns', 'swap_figures',
                        'see_two_cards', 'swap_card', 'through_wall']
        self.player_home_colors = ['home-red', 'home-yellow', 'home-green', 'home-blue']
        self.allowed_push_in_squares = ( (0,1),(0,3),(0,5),(1,0),(3,0),(5,0),
                                         (6,1),(6,3),(6,5),(1,6),(3,6),(5,6) )
        self.fixed_squares = ( (0,0), (2,0), (4,0), (6,0),
                               (0,2), (2,2), (4,2), (6,2),
                               (0,4), (2,4), (4,4), (6,4),
                               (0,6), (2,6), (4,6), (6,6) )
        self.corners = ( (0,0), (0,6), (6,0), (6,6) )
        self.movable_squares = tuple(set(self.board.keys()).difference(self.fixed_squares))
        
        # Game state
        self.current_tile = ''              #start tile obj
        self.last_pushed_in = (0,0)         #update every move
        self.last_pushed_out = (0,0)
        self.num_players = 3                #2,3,4 players
        
        # Initialise Game
        self.init_players()
        self.setup_tiles()
        self.load_images()
        self.setup_pygame()
        self.game_loop()
        
    def setup_pygame(self):
        """Setup Variables, Surfaces ,etc. for pygame"""
        
        # Initialise PyGame Variables
        pygame.init()
        self.mainscreen_size = (1100, 900)
        self.background_color = (127,255,212)
        self.is_hover = False
        
        self.screen = pygame.display.set_mode(
            self.mainscreen_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        
        self.game_area_x_offset = 200
        self.game_area_y_offset = 0
        self.game_area = self.screen.subsurface(
            Rect(self.game_area_x_offset,self.game_area_y_offset,900,900))
        
        self.board_area_x_offset = 100
        self.board_area_y_offset = 100
        self.board_area = self.game_area.subsurface(
            Rect(self.board_area_x_offset,self.board_area_y_offset,700,700))
            
        self.menu_area_x_offset = 0
        self.menu_area_y_offset = 0
        self.menu_area = self.screen.subsurface(
            Rect(self.menu_area_x_offset,self.menu_area_y_offset,200,900))
        
        self.tilerect = {}
        for square in self.board.keys():
            self.tilerect[square] = Rect(square[0]*100,square[1]*100,100,100)
            
        self.game_push_in_map = {(400, 800): (3, 6),
                                 (800, 600): (6, 5),
                                 (200, 0):   (1, 0),
                                 (200, 800): (1, 6),
                                 (800, 400): (6, 3),
                                 (0, 600):   (0, 5),
                                 (0, 200):   (0, 1),
                                 (0, 400):   (0, 3),
                                 (800, 200): (6, 1),
                                 (400, 0):   (3, 0),
                                 (600, 800): (5, 6),
                                 (600, 0):   (5, 0) }
        self.game_push_in_rects = (Rect(400, 800, 100, 100), Rect(800, 600, 100, 100),
                                   Rect(200, 0, 100, 100), Rect(200, 800, 100, 100),
                                   Rect(800, 400, 100, 100), Rect(0, 600, 100, 100),
                                   Rect(0, 200, 100, 100), Rect(0, 400, 100, 100),
                                   Rect(800, 200, 100, 100), Rect(400, 0, 100, 100),
                                   Rect(600, 800, 100, 100), Rect(600, 0, 100, 100) )
    def game_loop(self):
        self.display_everything()
        while 1:
            pygame.time.wait(100)
            #TODO fix cpu usage in loop
            #http://www.gamedev.net/topic/518494-pygame-eating-up-my-cpu/
            
            for event in pygame.event.get():
                #~ print event.type, event
                if event.type not in [pygame.QUIT, MOUSEBUTTONDOWN, MOUSEMOTION]:
                    continue 
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.mouse_over_push_in(event.pos)[0]:
                            self.current_tile.rotate()
                    elif event.button == 3:
                        if self.mouse_over_push_in(event.pos)[0]:
                            if self.mouse_over_push_in(event.pos)[2] != self.last_pushed_out:
                                self.push_in(self.mouse_over_push_in(event.pos)[2], self.current_tile)
                elif event.type == MOUSEMOTION:
                    is_hover = self.mouse_over_push_in(event.pos)
                    if is_hover[0]:
                        self.is_hover = is_hover[1]
                    else:
                        self.is_hover = False    
                    
                #TODO enable resize window.
                #http://stackoverflow.com/questions/20002242/how-to-scale-images-to-screen-size-in-pygame
                #~ elif event.type == VIDEORESIZE:
                    #~ self.screen = pygame.display.set_mode(
                        #~ event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    
            self.display_everything()
        
    def display_everything(self):
        """Draw everything to the screen"""
        #TODO subfunctions for display_tile, display_card
        
        def blit_tile(tile_obj, tile_rect, surface):
            """Blit a single tile with image
            tile_obj is a BoardTile instance
            tile_rect is the Rect obj
            surface is the surface to blit to
            """
            tile_image = pygame.image.fromstring(
                self.image_buffer[tile_obj.tile_type], (100,100), "RGBA")
            tile_rotation = tile_obj.tile_image_rotation()
            final_tile = pygame.transform.rotate(tile_image, tile_rotation)
            surface.blit(final_tile, tile_rect)
            
            if tile_obj.item:
                item = tile_obj.item
                item_image = pygame.image.fromstring(
                    self.image_buffer[item], (100,100), "RGBA")
                surface.blit(item_image, tile_rect)
            
        # Background
        self.screen.fill(self.background_color)
        
        # Board
        for square in self.board:
            #TODO Perf improve?: only blit rects where obj hash has changed
            # Tiles
            tile = self.board[square]
            rect = Rect(square[0]*100,square[1]*100,100,100)
            surf = self.board_area
            blit_tile(tile, rect, surf)
             
        # Push-In Squares at edges
        if self.is_hover:
            tile = self.current_tile
            rect = self.is_hover
            surf = self.game_area
            blit_tile(tile, rect, surf)
        
        # Labels
        myfont = pygame.font.SysFont("monospace", 15, bold=True)
        card_label = myfont.render("Current Card", 1, (0,0,0))
        tile_label = myfont.render("Current Tile", 1, (0,0,0))
        self.menu_area.blit(card_label, (50, 130))
        self.menu_area.blit(tile_label, (50, 255))
        
        # Current Card
        basecard_image = pygame.image.fromstring(
            self.image_buffer['basecard'], (100,100), "RGBA")
        basecard_rect = Rect(50,25,100,100)
        self.menu_area.blit(basecard_image, basecard_rect)
        player_item = self.current_player.cards[0]
        player_item_image = pygame.image.fromstring(
            self.image_buffer[player_item], (100,100), "RGBA")
        self.menu_area.blit(player_item_image, basecard_rect)
        
        # Current Tile
        tile = self.current_tile
        rect =  Rect(50,150,100,100)
        surf = self.menu_area
        blit_tile(tile, rect, surf)
        
        # Update display
        pygame.display.flip()
        
    def mouse_over_push_in(self, mouse_location):
        """Test if mouse hovering over a push in location
        Return tilerect or False
        """
        #~ mouse_location = (187,877)
        #~ _rect = (600, 800)
        
        mouse_x, mouse_y = mouse_location
        for _rect in self.game_push_in_rects:
            if _rect.collidepoint(mouse_x-200, mouse_y):
                _rectpos = (_rect.left,_rect.top)
                return (True, _rect, self.game_push_in_map[_rectpos])
        return (False,False)
        
    def print_board(self):
        """Print text representation of the board"""
        keys = sorted(self.board.keys())
        i, j = (0,7)
        while j < 50:
            for key in keys[i:j]:
                print self.board[key],
            print
            i += 7; j += 7
        print
        
    def push_in(self, push_in_square, tile):
        """Push tile into push_square
        Update row values
        Update current_tile
        """
        if push_in_square not in self.allowed_push_in_squares:
            raise Exception
        row_lists = { (0, 1): [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
                        (0, 3): [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3)],
                        (0, 5): [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)],
                        (1, 0): [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)],
                        (3, 0): [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)],
                        (5, 0): [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)],
                        (6, 1): [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)],
                        (6, 3): [(6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3), (0, 3)],
                        (6, 5): [(6, 5), (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5)],
                        (1, 6): [(1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0)],
                        (3, 6): [(3, 6), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (3, 0)],
                        (5, 6): [(5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0)] }
        row_vals = row_lists[push_in_square]
        
        #update current_tile
        self.current_tile = self.board[row_vals[-1]]
        
        #push new tile in and push tiles along
        for i in reversed(xrange(1,7)):
            cur_square = row_vals[i]
            pre_square = row_vals[i-1]
            pre_tile = self.board[pre_square]
            self.board[cur_square] = pre_tile
        self.board[row_vals[0]] = tile
        
        #Update last pushed in and out
        self.last_pushed_in = push_in_square
        self.last_pushed_out = row_lists[push_in_square][-1]
        
    def setup_tiles(self):
        """Initialise all tile objects
        Allocate tile objects to board positions
        """
        
        items_list = [i for i in self.items]                                   #each item once
        actions_list = [j for k in [[i,i] for i in self.actions] for j in k]   #each action twice
        colors_list = [i for i in self.player_home_colors]                          #each color once
        shuffle(items_list)
        shuffle(actions_list)
        
        ## Fixed Cards
        #corners
        self.board[(0,0)] = BoardTile([False,True,True,False])
        self.board[(0,6)] = BoardTile([True,True,False,False])
        self.board[(6,6)] = BoardTile([True,False,False,True])
        self.board[(6,0)] = BoardTile([False,False,True,True])
        
        #edges
        self.board[(0,2)] = BoardTile([True,True,True,False], item=items_list.pop())
        self.board[(2,0)] = BoardTile([False,True,True,True], item=items_list.pop())
        self.board[(4,0)] = BoardTile([False,True,True,True], item=items_list.pop())
        self.board[(0,4)] = BoardTile([True,True,True,False], item=items_list.pop())
        self.board[(6,2)] = BoardTile([True,False,True,True], item=items_list.pop())
        self.board[(2,6)] = BoardTile([True,True,False,True], item=items_list.pop())
        self.board[(6,4)] = BoardTile([True,False,True,True], item=items_list.pop())
        self.board[(4,6)] = BoardTile([True,True,False,True], item=items_list.pop())
        
        #centers
        self.board[(2,2)] = BoardTile([False,True,True,True], item=items_list.pop(), random_orientation=True)
        self.board[(4,2)] = BoardTile([False,True,True,True], item=items_list.pop(), random_orientation=True)
        self.board[(2,4)] = BoardTile([False,True,True,True], item=items_list.pop(), random_orientation=True)
        self.board[(4,4)] = BoardTile([False,True,True,True], item=items_list.pop(), random_orientation=True)
        ## Distributed Cards
        tiles = []
        #6 with three exits, all contain item, no actions
        for i in xrange(0,6):
            tiles.append(BoardTile([False,True,True,True], item=items_list.pop(), random_orientation=True))
        #6 straight through exits, no items, actions
        for i in xrange(0,6):
            tiles.append(BoardTile([False,True,False,True], action=actions_list.pop(), random_orientation=True))
        #6 straight through exits, no items, no actions
        for i in xrange(0,6):
            tiles.append(BoardTile([False,True,False,True], random_orientation=True))
        #6 corner exits, no items, contain actions
        for i in xrange(0,6):
            tiles.append(BoardTile([True,True,False,False], action=actions_list.pop(), random_orientation=True))
        #4 corner exits, no items, no actions
        for i in xrange(0,4):
            tiles.append(BoardTile([True,True,False,False], random_orientation=True))
        #6 corner exits, items, no actions
        for i in xrange(0,6):
            tiles.append(BoardTile([True,True,False,False], item=items_list.pop(), random_orientation=True))
            
        #Check all items and actions assigned
        if (len(items_list) or len(actions_list)) != 0:
            raise Exception
            
        #shuffle tiles before distributing to remaining board positions
        shuffle(tiles)

        #Assign tiles to remaining squares
        for square in self.movable_squares:
            self.board[square] = tiles.pop()
        
        #Remaining tile is the start tile
        self.current_tile = tiles.pop()
        
        # Set player home squares
        for square in ( (0,0), (0,6), (6,6), (6,0) ):
            self.board[square].item = colors_list.pop()
        
    def path_exists(self, square1, square2):
        """Determine if a path exists between two squares
        return True or False
        """
        pass
        # http://en.wikipedia.org/wiki/Tree_traversal
        # http://stackoverflow.com/questions/3097556/programming-theory-solve-a-maze
        # http://en.wikipedia.org/wiki/Breadth-first_search
        
    def init_players(self):
        """Initialise the players"""
        
        self.active_players = []
        ## Setup players
        self.player1 = Player()
        self.player2 = Player()
        self.player3 = Player()
        self.player4 = Player()
        # Activate players
        for i in xrange(0,self.num_players):
            [self.player1, self.player2, self.player3, self.player4][i].isactive = True
        # Player home squares
        self.player1.home = (0,0)
        self.player2.home = (0,6)
        self.player3.home = (6,0)
        self.player4.home = (6,6)
        # Player initial locations
        self.player1.location = self.player1.home
        self.player2.location = self.player2.home
        self.player3.location = self.player3.home
        self.player4.location = self.player4.home
        # Setup Cards
        self.cards_per_player = len(self.items)
        shuffle(self.items)
        hands = [self.items[i::self.num_players] for i in range(0, self.num_players)]
        for player in [self.player1, self.player2, self.player3, self.player4]:
            if player.isactive is True:
                self.active_players.append(player)
                player.cards = hands.pop()
        # Current Player to go
        self.current_player = self.active_players[0]
        
    def load_images(self):
        """Load tile images into string buffers"""
        
        image_path = {
                            'genie': os.path.join(self.image_dir, 'item-genie-100px.png'),
                            'map': os.path.join(self.image_dir, 'item-map-100px.png'),
                            'book': os.path.join(self.image_dir, 'item-book-100px.png'),
                            'bat': os.path.join(self.image_dir, 'item-bat-100px.png'),
                            'skull': os.path.join(self.image_dir, 'item-skull-100px.png'),
                            'ring': os.path.join(self.image_dir, 'item-ring-100px.png'),
                            'sword': os.path.join(self.image_dir, 'item-sword-100px.png'),
                            'candles': os.path.join(self.image_dir, 'item-candles-100px.png'),
                            'gem': os.path.join(self.image_dir, 'item-gem-100px.png'),
                            'lizzard': os.path.join(self.image_dir, 'item-lizzard-100px.png'),
                            'spider': os.path.join(self.image_dir, 'item-spider-100px.png'),
                            'purse': os.path.join(self.image_dir, 'item-purse-100px.png'),
                            'chest': os.path.join(self.image_dir, 'item-chest-100px.png'),
                            'beetle': os.path.join(self.image_dir, 'item-beetle-100px.png'),
                            'owl': os.path.join(self.image_dir, 'item-owl-100px.png'),
                            'keys': os.path.join(self.image_dir, 'item-keys-100px.png'),
                            'dwarf': os.path.join(self.image_dir, 'item-dwarf-100px.png'),
                            'helmet': os.path.join(self.image_dir, 'item-helmet-100px.png'),
                            'fairy': os.path.join(self.image_dir, 'item-fairy-100px.png'),
                            'moth': os.path.join(self.image_dir, 'item-moth-100px.png'),
                            'dragon': os.path.join(self.image_dir, 'item-dragon-100px.png'),
                            'mouse': os.path.join(self.image_dir, 'item-mouse-100px.png'),
                            'ghost': os.path.join(self.image_dir, 'item-ghost-100px.png'),
                            'crown': os.path.join(self.image_dir, 'item-crown-100px.png'),
                            'straight': os.path.join(self.image_dir, 'tile-tftf-100px.png'),
                            'corner': os.path.join(self.image_dir, 'tile-ttff-100px.png'),
                            'tee': os.path.join(self.image_dir, 'tile-ttft-100px.png'),
                            'home-red': os.path.join(self.image_dir, 'home-red-100px.png'),
                            'home-green': os.path.join(self.image_dir, 'home-green-100px.png'),
                            'home-blue': os.path.join(self.image_dir, 'home-blue-100px.png'),
                            'home-yellow': os.path.join(self.image_dir, 'home-yellow-100px.png'),
                            'basecard': os.path.join(self.image_dir, 'basecard-100px.png') }
        image_surface = {}
        for image in image_path.keys():
            image_surface[image] = pygame.image.load(image_path[image])
        self.image_buffer = {}
        for surface in image_surface.keys():
            self.image_buffer[surface] = pygame.image.tostring(image_surface[surface], "RGBA")
        
if __name__ == "__main__":
    MainWindow = NewGame()
    #~ MainWindow.MainLoop()        
