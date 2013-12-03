from player import Player
from graph import Graph

class ComputerPlayer(Player):
    def __init__(self, *args, **kwargs ):
        Player.__init__(self, *args, **kwargs)
        self.iscomputer = True
        
    def find_move(self, board):
        """Find the next move
        Return (rotation, push_in, new_square)"""
        pass
        
