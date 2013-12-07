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
        
    def possible_push_in(self, board):
        """Return list of possible push_in squares"""
        push_ins = set(board.allowed_push_in_squares)
        last = set(board.self.last_pushed_out,)
        return list(push_ins.difference(last))
