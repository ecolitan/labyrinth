# coding: utf8

class Graph:
    def __init__(self, board, square):
        """For a given board position and a square on the board,
        construct the graph of connected squares accessable from that square.
        """
        self.board = board
        self.square = square
        self.graph = {}
        self.queue = []
        self.build_graph()
       
    def build_graph(self):
        """Construct Graph data structure from board and square"""
        # http://www.python.org/doc/essays/graphs/
        # Data Structure of Graph
            # graph = {'A': ['B', 'C'],
            #          'B': ['C', 'D'],
            #          'C': ['D'],
            #          'D': ['C'],
            #          'E': ['F'],
            #          'F': ['C']}
            
        # For each exit from square,
        # if exit is not edge,
        # and if square opposite exit has matching exit
        # add that square to list for current square.
        
        # exits = [Up,Right,Down,Left]

        # Init loop
        self.queue.append(self.square)

        while len(self.queue) != 0:
            current_square = self.queue.pop()
            if self.square_in_graph_index(current_square):
                continue
            self.graph[current_square] = []
            for index in (0,1,2,3):
                if self.board[current_square].exits[index]:
                    possible_square = self.find_adjacent_square(current_square, index)
                    if possible_square is None:
                        continue
                    if self.path_connects(current_square, possible_square, index):
                        new_square = possible_square
                        if new_square not in self.queue:
                            self.queue.append(new_square)
                        self.graph[current_square].append(new_square)

    def find_adjacent_square(self, square, direction):
        """Find coords of the adjacent square in given direction
        Return coords of None if over egde.
        """
        # direction 0,1,2,3 -> [Up,Right,Down,Left]
        transform = ( (-1,0),(0,1),(1,0),(0,-1) )
        square_x, square_y = square
        trans_x, trans_y = transform[direction]
        new_square = (square_x+trans_x, square_y+trans_y)
        
        if (-1 or 7) in new_square:
            return None
        else:
            return new_square
        
    def path_connects(self ,square1, square2, direction):
        """Test if path connects two adjacent squares
        direction is the direction from square1 to square2
        Return True or False
        """
        reverse_direction_map = {0:2,1:3,2:0,3:1}
        if self.board[square1].exits[direction] and self.board[square2].exits[reverse_direction_map[direction]]:
            return True
        else:
            return False

    def square_in_graph_node(self, square):
        """Test if square is a node in the graph
        return True or False
        """
        for key in self.graph.keys():
            if square in self.graph[key]:
                return True
            else:
                return False
                
    def square_in_graph_index(self, square):
        """Test if square is an index in the graph
        Return True or False
        """
        for key in self.graph.keys():
            if key == square:
                return True
            else:
                return False

