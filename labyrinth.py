# coding: utf8

from random import shuffle
from player import Player
from tile import BoardTile
from graph import Graph

class NewGame:
    def __init__(self):
        """Setup the game"""
        
        # Board Grid
        self.board = { (0,0): None, (0,1): None, (0,2): None, (0,3): None, (0,4): None, (0,5): None, (0,6): None,
                       (1,0): None, (1,1): None, (1,2): None, (1,3): None, (1,4): None, (1,5): None, (1,6): None,
                       (2,0): None, (2,1): None, (2,2): None, (2,3): None, (2,4): None, (2,5): None, (2,6): None,
                       (3,0): None, (3,1): None, (3,2): None, (3,3): None, (3,4): None, (3,5): None, (3,6): None,
                       (4,0): None, (4,1): None, (4,2): None, (4,3): None, (4,4): None, (4,5): None, (4,6): None,
                       (5,0): None, (5,1): None, (5,2): None, (5,3): None, (5,4): None, (5,5): None, (5,6): None,
                       (6,0): None, (6,1): None, (6,2): None, (6,3): None, (6,4): None, (6,5): None, (6,6): None,}
        
        
        # List of items in game
        self.items = ['genie', 'map', 'book', 'bat', 'skull', 'ring', 'sword',
                      'candles', 'gem', 'lizzard', 'spider', 'purse', 'chest',
                      'beetle', 'owl', 'keys', 'dwarf', 'helmet', 'fairy',
                      'moth', 'dragon', 'mouse', 'ghost', 'crown']
        self.actions = ['second_push', 'two_turns', 'swap_figures',
                        'see_two_cards', 'swap_card', 'through_wall']
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
        self.num_players = 3                #2,3,4 players
        
        # Initialise Players
        self.init_players()
        
    def print_board(self):
        """Print representation of the board"""
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
        
        #Update last pushed in
        self.last_pushed_in = push_in_square
        
    def setup_tiles(self):
        """Initialise all tile objects
        Allocate tile objects to board positions
        """
        
        items_list = [i for i in self.items]                                   #each item once
        actions_list = [j for k in [[i,i] for i in self.actions] for j in k]   #each action twice
        shuffle(items_list)
        shuffle(actions_list)

        ## Fixed Cards
        #corners
        self.board[(0,0)] = BoardTile([False,True,True,False])
        self.board[(0,6)] = BoardTile([False,False,True,True])
        self.board[(6,6)] = BoardTile([True,False,False,True])
        self.board[(6,0)] = BoardTile([True,True,False,False])
        #edges
        self.board[(0,2)] = BoardTile([False,True,True,True], item=items_list.pop())
        self.board[(0,4)] = BoardTile([False,True,True,True], item=items_list.pop())
        self.board[(2,6)] = BoardTile([True,False,True,True], item=items_list.pop())
        self.board[(4,6)] = BoardTile([True,False,True,True], item=items_list.pop())
        self.board[(6,4)] = BoardTile([True,True,False,True], item=items_list.pop())
        self.board[(6,2)] = BoardTile([True,True,False,True], item=items_list.pop())
        self.board[(2,0)] = BoardTile([True,True,True,False], item=items_list.pop())
        self.board[(4,0)] = BoardTile([True,True,True,False], item=items_list.pop())
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
                player.cards = hands.pop()        
        
A=NewGame()
#~ A.setup_tiles()
#~ A.print_board_pickle()
