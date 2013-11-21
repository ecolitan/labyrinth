# coding: utf8

class Player:
    class_counter = 0
    def __init__(self):
        self.id = Player.class_counter
        Player.class_counter += 1
        
        self.isactive = False
        self.name = ''
        self.color = ''
        self.cards = []
        
    def __str__(self):
        return self.name
