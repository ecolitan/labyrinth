from player import Player
from graph import Graph
from copy import deepcopy

class ComputerPlayer(Player):
    def __init__(self, *args, **kwargs ):
        Player.__init__(self, *args, **kwargs)
        self.iscomputer = True
        
    def find_move(self, board):
        """Find the next move
        Return (rotation, push_in, new_square)"""
        working_board = deepcopy(board)
        #~ print "1", board, hash(board)
        #~ print "2", working_board, hash(working_board)
        board_queue = self.possible_push_in(working_board)
        
        graph = Graph(working_board)
        graph.build_graph(working_board.current_player.location)
        #~ print "9 comp is at", working_board.current_player.location
        
        while len(board_queue) != 0:
            #~ print "4", len(board_queue), board_queue
            push = board_queue.pop()
            result = self.evaluate_push(working_board, push, graph)
            if result:
                print "6", (push[0], push[1], result)
                print "8 computer searched for", board.current_player.current_card
                return (push[0], push[1], result)
        #~ print "7 computer searched for", board.current_player.current_card
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
        
    def evaluate_push(self, board, push_in, graph):
        """Evaluate a move for the current player of board
        Return square of item if found in current graph, or False
        """
        #~ print "3", push_in, type(push_in)
        board.current_tile.rotate_n_times(push_in[0])
        board.push_in(push_in[1])

        for square in board.keys():
            if board[square].item == board.current_player.current_card:
                #~ print "item found at", square
                if graph.travel_between(board.current_player.location, square):
                    #~ print "5", square
                    return square
        return False
