# coding: utf8
import sys
#~ import unittest
#~ import pickle
#~ from player import Player
#~ from tile import BoardTile
#~ from graph import Graph
#~ from labyrinth import NewGame

class GraphObj(dict):
    def __init__(self, *args, **kwargs ):
        dict.__init__(self, *args, **kwargs)
        
    def __hash__(self):
        """Hash a GraphObj"""
        contents = ([val for subl in self.keys() for val in subl] +
                    [val for subl in self.values() for val in subl])
        return hash(tuple(set(contents)))

class Graph:
    def __init__(self, board=None, square=None):
        """For a given board position and a square on the board,
        construct the graph of connected squares accessable from that square.
        """
        self.board = board
        #~ self.square = square
        self.all_graphs = []
        #~ self.graph = {}
        #~ self.queue = []
        #~ self.build_graph()
        self.build_all_graphs()
       
    def build_graph(self, square):
        """Construct a Graph data structure from starting square"""
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
        
        # Add initial square to the queue
        queue = []
        queue.append(square)
        graph = GraphObj()
        
        while len(queue) != 0:
            # Take current square for loop from the queue
            current_square = queue.pop()
            
            # If current square already an key, continue
            if self.square_in_graph_index(current_square, graph):
                continue
                
            # Add current square to graph
            graph[current_square] = []

            # For each direction
            for index in (0,1,2,3):
                
                # If there is an exit in that direction
                if self.board[current_square].exits[index]:
                    
                    # The possible square is the adjacent square in that direction
                    possible_square = self.find_adjacent_square(current_square, index)
                    
                    # If the edge of the board, continue the for current loop
                    if possible_square is None:
                        continue
                        
                    # If possible square already a key, continue
                    if self.square_in_graph_index(possible_square, graph):
                        continue
                        
                    # If a path connects the current to the possible square
                    if self.path_connects(current_square, possible_square, index):
                        # Set new square value 
                        new_square = possible_square
                        
                        # If new square not already in queue
                        if new_square not in queue:
                            # Add it to queue
                            queue.append(new_square)
                            
                        # Append new square to list for current square
                        graph[current_square].append(new_square)
                        
        # Remove empty nodes from graph
        for key in graph.keys():
            if graph[key] == []:
                del graph[key]
                
        return graph
                    
    def find_adjacent_square(self, square, direction):
        """Find coords of the adjacent square in given direction
        Return coords of None if over egde.
        """
        # direction 0,1,2,3 -> [Up,Right,Down,Left]
        transform = ( (0,-1),(1,0),(0,1),(-1,0) )       #(Up,Right,Down,Left)
        square_x, square_y = square
        trans_x, trans_y = transform[direction]
        new_square = (square_x+trans_x, square_y+trans_y)
        
        if ((-1 in new_square) or (7 in new_square)):
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

    def square_in_graph_node(self, square, graph):
        """Test if square is a node in the graph
        return True or False
        """
        for key in graph.keys():
            if square in graph[key]:
                return True
        return False
                
    def square_in_graph_index(self, square, graph):
        """Test if square is an index in the graph
        Return True or False
        """
        if square in graph:
            return True
        else:
            return False
            
    def square_in_graph(self, square, graph):
        """Test if a square is in a graph at all
        Return True or False
        """
        if ((self.square_in_graph_index(square, graph)) or
            self.square_in_graph_node(square, graph)):
            return True
        else:
            return False
        
    def travel_between_in_graph(self, square1, square2, graph):
        """Test if path between two squares in a graph
        Return True or False
        """
        if (self.square_in_graph(square1, graph) and self.square_in_graph(square2, graph)):
            return True
        else:
            return False
            
    def travel_between(self, square1, square2):
        """Test if path between two squares in any graph
        return True or False
        """
        for graph in self.all_graphs:
            if self.travel_between_in_graph(square1, square2, graph):
                return True
        return False
            
    def build_all_graphs(self):
        """Construct all Graphs from board"""
        for square in self.board:
            self.all_graphs.append(self.build_graph(square))
        self.remove_equivalent_graphs()
        
    def remove_equivalent_graphs(self):
        """Remove duplicate graphs from all_graphs
        if build_graphs() is working correctly, any two graphs which share a
        single node or index are duplicate for our purposes.
        """
        d = {}
        for x in self.all_graphs:
            d[x] = 1
        self.all_graphs = list(d.keys())
        
    def graph_exists(self, square):
        """Test if graph for a square exists
        Return True or False
        """
        for graph in self.all_graphs:
            if self.square_in_graph(square, graph):
                return False
        return True
