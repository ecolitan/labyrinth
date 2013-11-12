# coding: utf8

from random import randint

class BoardTile:
    class_counter = 0
    def __init__(self, exits, item=None, action=None, random_orientation=False):
        """A single square on the board"""
        self.id = BoardTile.class_counter
        BoardTile.class_counter += 1
        
        self.is_occupied = False
        self.item = item
        self.exits = exits                                # [Top,Right,Down,Left]
        self.action = action                              #hidden action on back of some cards
        if random_orientation:
            self.randomise_orientation()
        
    def __repr__(self):
        return self.item
        
    def __str__(self):
        return str(self.item)
        
    def rotate(self):
        """Rotate the exits 90deg clockwise"""
        r = self.exits.pop()
        self.exits.insert(0, r)
        
    def randomise_orientation(self):
        """Randomise the orientation of exits"""
        for _ in range(randint(0,3)):
            self.rotate()
