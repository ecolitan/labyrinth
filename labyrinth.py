# coding: utf8

import sys
import pygame
import os
import pickle
from pygame.locals import *
from random import shuffle
from player import Player
from tile import BoardTile
from graph import Graph
from board import Board
from computerplayer import ComputerPlayer
from startmenu import StartMenu

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class NewGame:
    def __init__(self, cli=False):
        """Setup the game"""
        
        # Misc Variables - all attributes registered in __init__()
        self.image_dir = 'images'
        self.cli = cli
        self.image_buffer = {}
        
        # Board Grid (x right, y down)       
        self.board = Board({
            (0,0): None, (1,0): None, (2,0): None, (3,0): None, (4,0): None, (5,0): None, (6,0): None,
            (0,1): None, (1,1): None, (2,1): None, (3,1): None, (4,1): None, (5,1): None, (6,1): None,
            (0,2): None, (1,2): None, (2,2): None, (3,2): None, (4,2): None, (5,2): None, (6,2): None,
            (0,3): None, (1,3): None, (2,3): None, (3,3): None, (4,3): None, (5,3): None, (6,3): None,
            (0,4): None, (1,4): None, (2,4): None, (3,4): None, (4,4): None, (5,4): None, (6,4): None,
            (0,5): None, (1,5): None, (2,5): None, (3,5): None, (4,5): None, (5,5): None, (6,5): None,
            (0,6): None, (1,6): None, (2,6): None, (3,6): None, (4,6): None, (5,6): None, (6,6): None,})
        
        # List of items in game
        self.items = [
            'genie', 'map', 'book', 'bat', 'skull', 'ring', 'sword',
            'candles', 'gem', 'lizzard', 'spider', 'purse', 'chest',
            'beetle', 'owl', 'keys', 'dwarf', 'helmet', 'fairy',
            'moth', 'dragon', 'mouse', 'ghost', 'crown']
        self.actions = [
            'second_push', 'two_turns', 'swap_figures',
            'see_two_cards', 'swap_card', 'through_wall']
        self.player_home_colors = [
            'home-red', 'home-yellow', 'home-green', 'home-blue']
        
        # Game state
        self.num_human_players = 1          #2,3,4 players
        self.num_computer_players = 1       #2,3,4 players
        if not (2 <= (self.num_human_players + self.num_computer_players) <= 4):
            raise Exception("2 - 4 players allowed only")
        
        self.game_phase = 'start'            #start -> (rotate) + "push" -> "move" ->
        self.text_message_box = {
            'start': 'Click start to begin!',
            'push': 'Hover the mouse over the push-in square. Rotate the tile with left-click. Right-Click to push tile in.',
            'move': 'Click a square to move there.',
            'won': 'You Won!!' }
        self.game_history = []
        self.move_number = 0
        
        if self.cli == False:
            self.setup_pygame()
            self.game_loop()
        
    def setup_pygame(self):
        """Setup Variables, Surfaces ,etc. for pygame"""
        
        # Initialise PyGame Variables
        pygame.init()
        self.mainscreen_size = (1100, 900)
        self.background_color = (160,217,92)
        self.menu_background_color = (71,163,255)
        self.start_button_color = (255,0,0)
        self.menu_button_color = (71,163,255)
        self.color_push_in_rect = (153,255,179)
        self.color_no_push_in = (204,0,0)
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
            
        self.game_push_in_map = {
            (400, 800): (3, 6),
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
        self.inv_push_in_map = {v:k for k, v in self.game_push_in_map.items()}
        self.game_push_in_rects = (
            Rect(400, 800, 100, 100),
            Rect(800, 600, 100, 100),
            Rect(200, 0, 100, 100),
            Rect(200, 800, 100, 100),
            Rect(800, 400, 100, 100),
            Rect(0, 600, 100, 100),
            Rect(0, 200, 100, 100),
            Rect(0, 400, 100, 100),
            Rect(800, 200, 100, 100),
            Rect(400, 0, 100, 100),
            Rect(600, 800, 100, 100),
            Rect(600, 0, 100, 100) )
            
        self.menu = StartMenu(self.screen)
            
    def game_loop(self):
        """Game loop for capturing user input, displaying screens,
        updating players and squares.
        """
        
        def process_human_move():
            pygame.time.wait(100)
            for event in pygame.event.get():
                if event.type not in [pygame.QUIT, MOUSEBUTTONDOWN, MOUSEMOTION]:
                    continue 
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.game_phase == "push":
                            if self.mouse_over_push_in(event.pos)[0]:
                                self.board.current_tile.rotate()
                        elif self.game_phase == "move":
                            square = self.mouse_over_board(event.pos)
                            if square:
                                #TODO function for this?
                                if self.board.path_exists(
                                    self.board.current_player.location, square):
                                    self.board.update_player_location(
                                        self.board.current_player, square)
                                    if self.board.update_player_item(self.board.current_player, square) == "winner":
                                        self.game_phase == "won"
                                    self.board.next_active_player()
                                    self.game_phase = "push"
                                    self.game_history.append(self.board)
                                    self.move_number += 1
                    elif event.button == 3:
                        if self.game_phase == "push":
                            if self.mouse_over_push_in(event.pos)[0]:
                                if self.mouse_over_push_in(event.pos)[2] != self.board.last_pushed_out:
                                    self.board.push_in(self.mouse_over_push_in(event.pos)[2])
                                    self.game_phase = "move"
                            
                elif event.type == MOUSEMOTION:
                    is_hover = self.mouse_over_push_in(event.pos)
                    if is_hover[0]:
                        self.is_hover = is_hover[1]
                    else:
                        self.is_hover = False    
            self.display_everything()
            
        def process_computer_move():
            if self.game_phase == "push":
                
                #do push and move together
                #~ print "before find_move", hash(self.board)
                rotation, push_in, new_square = self.board.current_player.find_move(self.board)
                #~ rotation, push_in, new_square = (0, (1,0), self.board.current_player.location)
                #~ print "after find_move", hash(self.board)
                
                self.board.current_tile.rotate_n_times(rotation)
                self.board.push_in(push_in)
                #~ pygame.time.wait(2000)
                self.board.update_player_location(self.board.current_player, new_square)
                if self.board.update_player_item(self.board.current_player, new_square) == "winner":
                    self.game_phase = "won"
                self.board.next_active_player()
                self.game_history.append(self.board)
                self.move_number += 1
                self.display_everything()
            
        def collect_start_screen_input():
            pygame.time.wait(100)
            for event in pygame.event.get():
                if event.type not in [pygame.QUIT, MOUSEBUTTONDOWN, MOUSEMOTION]:
                    continue 
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.menu.mouse_click_button(event.pos) is True:
                            self.num_computer_players = self.menu.n_players
                            self.num_players = (
                                self.num_human_players + self.num_computer_players)
                            #~ print self.num_players, self.num_human_players, self.num_computer_players
                            # Initialise Game
                            self.setup_tiles()
                            #players must be setup after tiles
                            self.init_players()
                            self.load_images()
                            self.game_phase = "push"
            self.menu.display_menu()
        
        self.game_history.append(self.board)    
        self.menu.display_menu()
        # Game Loop
        while 1:
            if self.game_phase == "start":
                collect_start_screen_input()
            elif self.game_phase == "won":
                self.display_everything().game_over_screen()
            elif (self.game_phase == "move" and not
                  self.board.possible_moves_exist(self.board.current_player)):
                self.board.next_active_player()
                self.game_phase = "push"
                self.game_history.append(self.board)
                self.move_number += 1
            elif self.board.current_player.iscomputer is False:
                process_human_move()
            elif self.board.current_player.iscomputer is True:
                process_computer_move()
        
    def display_everything(self):
        """Draw everything to the screen"""
        
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
                
        def blit_card(card, card_rect, surface):
            """Blit a single card
            str card
            Rect card_rect
            Surface surface
            """
            basecard_image = pygame.image.fromstring(
                self.image_buffer['basecard'], (100,100), "RGBA")
            surface.blit(basecard_image, card_rect)
            card_image = pygame.image.fromstring(
                self.image_buffer[card], (100,100), "RGBA")
            surface.blit(card_image, card_rect)
            
        def blit_player(player_obj, surface, coords=None):
            """Blit a player figure to the board"""
            if coords == None:
                coords = (player_obj.location[0]*100, player_obj.location[1]*100)
            dims = (100,100)
            
            player_color = player_obj.color
            player_figure = player_obj.player_images[player_color]
            player_image = pygame.image.fromstring(
                self.image_buffer[player_figure], (100,100), "RGBA")
            player_square = player_obj.location
            player_rect = Rect((coords),(dims))
            surface.blit(player_image, player_rect)
            
        def blit_text(surface, text, color, rect, font, aa=False, bkg=None):
            """Draw some text into an area of a surface
            automatically wraps words
            returns any text that didn't get blitted
            """
            rect = Rect(rect)
            y = rect.top
            lineSpacing = -2
         
            # get the height of the font
            fontHeight = font.size("Tg")[1]
         
            while text:
                i = 1
         
                # determine if the row of text will be outside our area
                if y + fontHeight > rect.bottom:
                    break
         
                # determine maximum width of line
                while font.size(text[:i])[0] < rect.width and i < len(text):
                    i += 1
         
                # if we've wrapped the text, then adjust the wrap to the last word      
                if i < len(text): 
                    i = text.rfind(" ", 0, i) + 1
         
                # render the line and blit it to the surface
                if bkg:
                    image = font.render(text[:i], 1, color, bkg)
                    image.set_colorkey(bkg)
                else:
                    image = font.render(text[:i], aa, color)
         
                surface.blit(image, (rect.left, y))
                y += fontHeight + lineSpacing
         
                # remove the text we just blitted
                text = text[i:]
            return text
            
        def blit_push_in_rect(surface, color, rect):
            """push in rects are green
            except the one where you may not push!
            """
            pygame.draw.rect(surface, color, rect)
            
        def game_over_screen():
            """Blit a final screen for game over"""
            self.screen.fill(self.background_color)
            blit_text(
                self.screen,
                "Game Over!",
                (0,0,0),
                (400,500,190,190),
                myfont )
            raw_input()
        
        # Background
        self.screen.fill(self.background_color)
        self.menu_area.fill(self.menu_background_color)
        
        # Board
        for square in self.board:
            #TODO Perf improve?: only blit rects where obj hash has changed
            # Tiles
            tile = self.board[square]
            rect = Rect(square[0]*100,square[1]*100,100,100)
            surf = self.board_area
            blit_tile(tile, rect, surf)
                
        # Player Figures
        for player in self.board.active_players:
            blit_player(player, self.board_area)
             
        # Push-In Squares at edges
        if self.board.last_pushed_out:
            last_pushed_out = self.board.last_pushed_out
            last_pushed_out_rect = Rect(
                (self.inv_push_in_map[last_pushed_out]), (100,100))
            blit_push_in_rect(
                self.game_area, self.color_no_push_in, last_pushed_out_rect)
        else:
            last_pushed_out_rect = None
            
        for rect in self.game_push_in_rects:
            if ((rect != self.is_hover) and (rect != last_pushed_out_rect)):
                blit_push_in_rect(self.game_area, self.color_push_in_rect, rect)
                
        if (self.is_hover and self.is_hover != last_pushed_out_rect):
            tile = self.board.current_tile
            rect = self.is_hover
            surf = self.game_area
            blit_tile(tile, rect, surf)
        
        # Labels
        myfont = pygame.font.SysFont("monospace", 15, bold=True)
        card_label = myfont.render("Current Card", 1, (0,0,0))
        tile_label = myfont.render("Current Tile", 1, (0,0,0))
        player_label = myfont.render(
            "Current Player: {}".format(self.board.current_player.color), 1, (0,0,0))
        player_remaining_cards = myfont.render(
            "Cards: {}".format(
                self.board.current_player.remaining_cards()), 1, (0,0,0))
        self.menu_area.blit(card_label, (50, 130))
        self.menu_area.blit(tile_label, (50, 255))
        self.menu_area.blit(player_label, (5, 380))
        self.menu_area.blit(player_remaining_cards, (5, 395))
        
        # Current Card
        card = self.board.current_player.current_card
        rect = Rect(50,25,100,100)
        surf = self.menu_area
        blit_card(card, rect, surf)
        
        # Current Tile
        tile = self.board.current_tile
        rect =  Rect(50,150,100,100)
        surf = self.menu_area
        blit_tile(tile, rect, surf)
        
        # Current Player in menu
        blit_player(self.board.current_player, self.menu_area, (50,275))
        
        # Text box
        blit_text(self.menu_area, self.text_message_box[self.game_phase],
            (0,0,0), (5,500,190,190), myfont)
            
        # Game Border
        border_color = (0,0,0)
        game_area_rect = (0,0,900,900)
        border_width = 4
        pygame.draw.rect(self.game_area, border_color, game_area_rect, border_width)
        
        # Update display
        pygame.display.flip()
            
    def mouse_over_push_in(self, mouse_location):
        """Test if mouse hovering over a push in location
        Return (True|False, tilerect, square)
        """
        mouse_x, mouse_y = mouse_location
        for _rect in self.game_push_in_rects:
            if _rect.collidepoint(mouse_x-200, mouse_y):
                _rectpos = (_rect.left,_rect.top)
                return (True, _rect, self.game_push_in_map[_rectpos])
        return (False,False,False)
        
    def mouse_over_board(self, mouse_location):
        """Test if mouse over the board
        Return square or False
        """
        mouse_x, mouse_y = mouse_location
        if not ((300 <= mouse_x < 1000) and (100 <= mouse_y < 800)):
            return False
        else:
            x_pos = (mouse_x - 300) / 100
            y_pos = (mouse_y - 100) / 100
            return (x_pos,y_pos)
        
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
        if len(items_list) != 0:
            raise Exception("Leftover tiles!")
        if len(actions_list) != 0:
            raise Exception("Leftover actions!")
            
        #shuffle tiles before distributing to remaining board positions
        shuffle(tiles)

        #Assign tiles to remaining squares
        for square in self.board.movable_squares:
            self.board[square] = tiles.pop()
        
        #Remaining tile is the start tile
        self.board.current_tile = tiles.pop()
        
        # Set player home squares
        for square in ( (0,0), (0,6), (6,6), (6,0) ):
            self.board[square].item = colors_list.pop()
        
    def init_players(self):
        """Initialise the human and computer player objects
        2 <= (Human players + Computer players) <= 4
        """
        ## Setup players
        available_color_locations = [('blue',   (0,0)),
                                     ('red',    (6,0)),
                                     ('green',  (0,6)),
                                     ('yellow', (6,6)) ]
        human_players = []
        computer_players = []
        
        for i in xrange(0, self.num_human_players):
            player = Player(available_color_locations.pop())
            player.isactive = True
            human_players.append(player)
            
        for i in xrange(0, self.num_computer_players):
            player = ComputerPlayer(available_color_locations.pop())
            player.isactive = True
            computer_players.append(player)
            
        self.board.active_players = computer_players + human_players
            
        # Setup Cards
        self.cards_per_player = len(self.items)
        shuffle(self.items)
        hands = [self.items[i::self.num_players] for i in range(0, self.num_players)]
        
        for player in self.board.active_players:
            player.cards = hands.pop()
            player.draw_card()
                
        # Set squares to occupied
        for player in self.board.active_players:
            self.board[player.location].add_resident(player)
        
        # Current Player to go
        self.board.current_player = self.board.active_players[0]
        
        # Generate test object for unittest - remove later
        #~ _f = open("testPlayer2.pickle", "a")
        #~ self.board.next_active_player()
        #~ pickle.dump(self.board.current_player, _f, pickle.HIGHEST_PROTOCOL)
        #~ _f.close
        #~ print self.board.current_player.isactive
        #~ print self.board.current_player.name
        #~ print self.board.current_player.color
        #~ print self.board.current_player.cards
        #~ print self.board.current_player.location
        #~ print self.board.current_player.home
        #~ print self.board.current_player.current_card
        #~ print self.board.current_player.found_cards
        #~ print self.board.current_player.iscomputer
        #~ print self.board.current_player.__str__()
        #~ print self.board.current_player.__hash__()
        #~ print hash(self.board.current_player)
        
        
    def load_images(self):
        """Load tile images into string buffers
        store buffers in the dict self.image_buffer
        """
        image_filename = {
                            'genie': 'item-genie-100px.png',
                            'map': 'item-map-100px.png',
                            'book': 'item-book-100px.png',
                            'bat': 'item-bat-100px.png',
                            'skull': 'item-skull-100px.png',
                            'ring': 'item-ring-100px.png',
                            'sword': 'item-sword-100px.png',
                            'candles': 'item-candles-100px.png',
                            'gem': 'item-gem-100px.png',
                            'lizzard': 'item-lizzard-100px.png',
                            'spider': 'item-spider-100px.png',
                            'purse': 'item-purse-100px.png',
                            'chest': 'item-chest-100px.png',
                            'beetle': 'item-beetle-100px.png',
                            'owl': 'item-owl-100px.png',
                            'keys': 'item-keys-100px.png',
                            'dwarf': 'item-dwarf-100px.png',
                            'helmet': 'item-helmet-100px.png',
                            'fairy': 'item-fairy-100px.png',
                            'moth': 'item-moth-100px.png',
                            'dragon': 'item-dragon-100px.png',
                            'mouse': 'item-mouse-100px.png',
                            'ghost': 'item-ghost-100px.png',
                            'crown': 'item-crown-100px.png',
                            'straight': 'tile-tftf-100px.png',
                            'corner': 'tile-ttff-100px.png',
                            'tee': 'tile-ttft-100px.png',
                            'home-red': 'home-red-100px.png',
                            'home-green': 'home-green-100px.png',
                            'home-blue': 'home-blue-100px.png',
                            'home-yellow': 'home-yellow-100px.png',
                            'basecard': 'basecard-100px.png',
                            'player-yellow': 'player-yellow-100px.png',
                            'player-blue': 'player-blue-100px.png',
                            'player-green': 'player-green-100px.png',
                            'player-red': 'player-red-100px.png' }
        image_surface = {}
        for image in image_filename.keys():
            image_surface[image] = pygame.image.load(
                os.path.join(self.image_dir, image_filename[image]))
        for surface in image_surface.keys():
            self.image_buffer[surface] = pygame.image.tostring(image_surface[surface], "RGBA")
        
if __name__ == "__main__":
    MainWindow = NewGame()

