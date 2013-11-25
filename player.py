# coding: utf8

class Player:
    class_counter = 0
    def __init__(self, color, location):
        self.id = Player.class_counter
        Player.class_counter += 1
        
        self.isactive = False
        self.name = ''
        self.color = color
        self.cards = []
        self.location = location
        self.home = location
        
        self.player_images = {'yellow': 'player-yellow',
                              'blue': 'player-blue',
                              'green': 'player-green',
                              'red': 'player-red'}
    def __str__(self):
        return self.color
