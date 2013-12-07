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
        push_in_queue = self.possible_push_in(board)
        
        
    def possible_push_in(self, board):
        """Generate possible push_in squares combined with possible orientations
        Return list of tuples [ ( square x,y , orientaion 0|1|2|3 ) ]
        """
        output_list = []
        push_ins = set(board.allowed_push_in_squares)
        last = set(board.self.last_pushed_out,)
        for push in push_ins.difference(last):
            for i in xrange(0,4):
                output_list.append((push, i))
        return output_list
        
    def find_item(self, board, push_in):
        """Attepmt to find item for current player
        Return square of item if found, or false
        """
        board.current_tile.rotate_n_times(push_in[1])
        board.push_in(push_in[0])
        graph = Graph(board)
        graph.build_graph(board.current_player.location)
        for square in board:
            if square.item == board.current_player.current_card:
                if graph.travel_between(board.current_player.location, square):
                    return square
        return False
