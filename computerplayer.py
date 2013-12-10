from player import Player
from graph import Graph

class ComputerPlayer(Player):
    def __init__(self, *args, **kwargs ):
        Player.__init__(self, *args, **kwargs)
        self.iscomputer = True
        
    def find_move(self, board):
        """Find the next move
        Return (rotation, push_in, new_square)"""
        #~ board_queue = self.possible_push_in(board)
        
        #~ while len(board_queue) != 0:
            #~ push = board_queue.pop()
            #~ result = self.evaluate_push(board, push)
            #~ if type(result) is tuple:
                #~ return (push[0], push[1], result)
            #~ elif type(result) is list:
                #~ board_queue += result
        return (0, (1,0), board.current_player.location)
            
            
    def possible_push_in(self, board):
        """Generate possible push_in squares combined with possible orientations
        Return list of tuples [ ( orientaion 0|1|2|3 , square x,y ) ]
        """
        output_list = []
        push_ins = set(board.allowed_push_in_squares)
        last = set((board.last_pushed_out,))
        for push in push_ins.difference(last):
            for rotation in xrange(0,4):
                output_list.append((rotation, push))
        return output_list
        
    def evaluate_push(self, board, push_in):
        """Evaluate a move for the current player of board
        Return square of item if found, or moves list
        """
        moves_list = []
        board.current_tile.rotate_n_times(push_in[0])
        board.push_in(push_in[1])
        graph = Graph(board)
        graph.build_graph(board.current_player.location)
        for square in board.keys():
            if board[square].item == board.current_player.current_card:
                if graph.travel_between(board.current_player.location, square):
                    return square
                else:
                    moves_list.append(
                        board.update_player_location(
                            board.current_player, square))
        return moves_list
