# coding: utf8
import sys
#~ import unittest
#~ import pickle
#~ from player import Player
#~ from tile import BoardTile
#~ from graph import Graph
#~ from labyrinth import NewGame

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
        
        # Add initial square to the queue
        self.queue.append(self.square)
        
        while len(self.queue) != 0:
            # Take current square for loop from the queue
            current_square = self.queue.pop()
            
            # If current square already an key, continue
            if self.square_in_graph_index(current_square):
                continue
                
            # Add current square to graph
            self.graph[current_square] = []

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
                    if self.square_in_graph_index(possible_square):
                        continue
                        
                    # If a path connects the current to the possible square
                    if self.path_connects(current_square, possible_square, index):
                        # Set new square value 
                        new_square = possible_square
                        
                        # If new square not already in queue
                        if new_square not in self.queue:
                            # Add it to queue
                            self.queue.append(new_square)
                            
                        # Append new square to list for current square
                        self.graph[current_square].append(new_square)
                        
        # Remove empty nodes from graph
        for key in self.graph.keys():
            if self.graph[key] == []:
                del self.graph[key]
                    
    def find_adjacent_square(self, square, direction):
        """Find coords of the adjacent square in given direction
        Return coords of None if over egde.
        """
        # direction 0,1,2,3 -> [Up,Right,Down,Left]
        transform = ( (0,-1),(1,0),(0,1),(-1,0) )       #(Up,Right,Down,Left)
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
        print "square1", square1
        print "square2", square2
        reverse_direction_map = {0:2,1:3,2:0,3:1}
        if self.board[square1].exits[direction] and self.board[square2].exits[reverse_direction_map[direction]]:
            return True
        else:
            return False

    def square_in_graph_node(self, square, graph=None):
        """Test if square is a node in the graph
        return True or False
        """
        if graph:
            _graph = graph
        else:
            _graph = self.graph
            
        for key in _graph.keys():
            if square in _graph[key]:
                return True
        return False
                
    def square_in_graph_index(self, square, graph=None):
        """Test if square is an index in the graph
        Return True or False
        """
        if graph:
            _graph = graph
        else:
            _graph = self.graph
            
        if square in _graph:
            return True
        else:
            return False
        
    def travel_between(self, square1, square2, graph=None):
        """Test if path between two squares in a graph
        Return True or False
        """
        pass
        if graph:
            _graph = graph
        else:
            _graph = self.graph
            
        if ((self.square_in_graph_index(square1, _graph) or self.square_in_graph_node(square1, _graph)) and
            (self.square_in_graph_index(square2, _graph) or self.square_in_graph_node(square2, _graph))):
            return True
        else:
            return False
