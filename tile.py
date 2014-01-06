# coding: utf8

from random import randint

class BoardTile:
    class_counter = 0
    def __init__(self, exits, item=None, action=None, random_orientation=False):
        """A single square on the board"""
        
        # Incrementing object id
        self.id = BoardTile.class_counter
        BoardTile.class_counter += 1
        
        # Basic tile attributes
        self.is_occupied = False
        self.item = item
        self.exits = exits                                # [Top,Right,Down,Left]
        self.action = action                              # hidden action on back of some cards
        self.occupied_by = []
        
        # Set orientation
        if random_orientation:
            self.randomise_orientation()
        
        # Set tile image attribute
        self.tile_type = self.determine_tile_type()
        self.tile_images = {'straight': 'tile-tftf-100px.png',
                            'corner': 'tile-ttff-100px.png',
                            'tee': 'tile-ttft-100px.png' }
        self.tile_image = self.tile_images[self.tile_type]
        
        # Set item image attrribute
        self.item_images = {'genie': 'genie-ghost-100px.png',
                            'map': 'map-ghost-100px.png',
                            'book': 'book-ghost-100px.png',
                            'bat': 'bat-ghost-100px.png',
                            'skull': 'skull-ghost-100px.png',
                            'ring': 'ring-ghost-100px.png',
                            'sword': 'sword-ghost-100px.png',
                            'candles': 'candles-ghost-100px.png',
                            'gem': 'gem-ghost-100px.png',
                            'lizzard': 'lizzard-ghost-100px.png',
                            'spider': 'spider-ghost-100px.png',
                            'purse': 'purse-ghost-100px.png',
                            'chest': 'chest-ghost-100px.png',
                            'beetle': 'beetle-ghost-100px.png',
                            'owl': 'owl-ghost-100px.png',
                            'keys': 'keys-ghost-100px.png',
                            'dwarf': 'dwarf-ghost-100px.png',
                            'helmet': 'helmet-ghost-100px.png',
                            'fairy': 'fairy-ghost-100px.png',
                            'moth': 'moth-ghost-100px.png',
                            'dragon': 'dragon-ghost-100px.png',
                            'mouse': 'mouse-ghost-100px.png',
                            'ghost': 'ghost-ghost-100px.png',
                            'crown': 'crown-ghost-100px.png',
                            'home-red': 'home-red-100px.png',
                            'home-green': 'home-green-100px.png',
                            'home-blue': 'home-blue-100px.png',
                            'home-yellow': 'home-yellow-100px.png' }
        if self.item:
            self.item_image = self.item_images[self.item]
        else:
            self.item_image = None
            
    def __repr__(self):
        return self.item
        
    def __str__(self):
        return str(self.item)
        
    def __hash__(self):
        return hash((self.id, self.is_occupied, tuple(self.exits), self.action, self.item))
        
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
        
    def __ne__(self,other):
        return self.__hash__() != other.__hash__()
        
    def rotate(self):
        """Rotate the exits 90deg clockwise"""
        r = self.exits.pop()
        self.exits.insert(0, r)
        
    def rotate_n_times(self, n):
        """Rotate the exits 90deg clockwise n times
        n in (0,1,2,3)
        """
        if n not in (0,1,2,3):
            raise Exception("Invalid rotation number")
            
        for i in xrange(0,n):
            self.rotate()
        
    def randomise_orientation(self):
        """Randomise the orientation of exits"""
        for _ in range(randint(0,3)):
            self.rotate()
        
    def determine_tile_type(self):
        """Determine type of tile from exits
        return 'straight'|'corner'|'tee'
        """
        if self.exits in ([True,True,False,False],[False,True,True,False],
                     [False,False,True,True],[True,False,False,True]):
            return 'corner'
        elif self.exits in ([True,False,True,False],[False,True,False,True]):
            return 'straight'
        else:
            return 'tee'
        
    def tile_image_rotation(self):
        """Return the correct rotation of the tile image.
        Return 0|90|180|270
        """
        orientations = {    tuple([True,True,False,False]): 0,
                            tuple([False,True,True,False]): -90,
                            tuple([False,False,True,True]): -180,
                            tuple([True,False,False,True]): -270,
                            tuple([True,False,True,False]): 0,
                            tuple([False,True,False,True]): -90,
                            tuple([True,True,False,True]): 0,
                            tuple([True,True,True,False]): -90,
                            tuple([False,True,True,True]): -180,
                            tuple([True,False,True,True]): -270 }
        return orientations[tuple(self.exits)]
        
    def add_resident(self, player):
        """Add a player to the occupied_by list
        update is_occupied
        return occupied_by List
        """
        if player not in self.occupied_by:
            self.occupied_by.append(player)
        self.is_occupied = True
        return self.occupied_by
            
    def del_resident(self, player):
        """Remove a player from the occupied_by list
        update is_occupied
        return Player removed or None
        """
        if player in self.occupied_by:
            self.occupied_by.remove(player)
            if len(self.occupied_by) == 0:
                self.is_occupied = False
            return player
        return None
