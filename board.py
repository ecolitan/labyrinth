# coding: utf8

from graph import Graph

class Board(dict):
    def __init__(self, *args, **kwargs ):
        dict.__init__(self, *args, **kwargs)
        
        self.current_tile = ''
        self.fixed_squares = ( (0,0), (2,0), (4,0), (6,0),
                               (0,2), (2,2), (4,2), (6,2),
                               (0,4), (2,4), (4,4), (6,4),
                               (0,6), (2,6), (4,6), (6,6) )
        self.movable_squares = tuple(
            set(self.keys()).difference(self.fixed_squares))
        self.corners = ( (0,0), (0,6), (6,0), (6,6) )
        self.allowed_push_in_squares = ( (0,1),(0,3),(0,5),(1,0),(3,0),(5,0),
                                         (6,1),(6,3),(6,5),(1,6),(3,6),(5,6) )
        self.last_pushed_in = False              #update every move
        self.last_pushed_out = False             #update every move
        self.row_lists = { 
            (0, 1): [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
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
        self.active_players = []
        self.current_player = None
        
    def __hash__(self):

        hash_list = []

        # hash tile objects together
        for tile in sorted(self.values()):
            hash_list.append(tile)
        hash_list.append(self.current_tile)
        hash_list.append(self.last_pushed_in)
        hash_list.append(self.last_pushed_out)
        
        # players
        for player in self.active_players:
            hash_list.append(player)
        hash_list.append(self.current_player)
        return hash(tuple(hash_list))
        
    def push_in(self, push_in_square):
        """Push tile into push_square
        Update row values
        Update current_tile
        """
        if push_in_square not in self.allowed_push_in_squares:
            raise Exception
        
        row_vals = self.row_lists[push_in_square]
        
        #update current_tile
        next_current_tile = self[row_vals[-1]]
        
        #push new tile in and push tiles along
        for i in reversed(xrange(1,7)):
            cur_square = row_vals[i]
            pre_square = row_vals[i-1]
            pre_tile = self[pre_square]
            self[cur_square] = pre_tile
        self[row_vals[0]] = self.current_tile
        self.current_tile = next_current_tile
        
        #Update last pushed in and out
        self.last_pushed_in = push_in_square
        self.last_pushed_out = self.row_lists[push_in_square][-1]
        
        # Update player positions on the pushed row
        self.update_pushed_players(push_in_square)
        
    def print_board(self):
        """Print text representation of the board"""
        keys = sorted(self.keys())
        i, j = (0,7)
        while j < 50:
            for key in keys[i:j]:
                print self[key],
            print
            i += 7; j += 7
        print
        
    def update_player_location(self, player_obj, square):
        """Update all the variables needed to move player to another square"""
        self[player_obj.location].del_resident(player_obj)
        player_obj.location = square
        self[square].add_resident(player_obj)
            
    def update_pushed_players(self, push_in_square):
        """Update locations of any players standing on a pushed row"""
        for player in self.active_players:
            if player.location == self.last_pushed_out:
                self.update_player_location(player, self.last_pushed_in)
            elif player.location in self.row_lists[push_in_square]:
                index = self.row_lists[push_in_square].index(player.location)
                self.update_player_location(
                    player, self.row_lists[push_in_square][index + 1])
                
    def next_active_player(self):
        """Change self.current_player to the next active player"""
        p = self.active_players.pop()
        self.active_players.insert(0, p)
        self.current_player = self.active_players[0]
                
    def update_player_item(self, player_obj, square):
        """Update the players item attributes
        Return winner if no more items for player
        """
        if self[square].item == player_obj.current_card:
            return player_obj.current_card_found()
            
    def path_exists(self, square1, square2):
        """Use graph to test if a path exists between two squares"""
        return (Graph(self).
            travel_between(square1, square2))
            
    def possible_moves_exist(self, player_obj):
        """Check if possible moves available
        return True or False
        """
        return (Graph(self).
            graph_exists(player_obj.location))
            
