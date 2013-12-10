# coding: utf8

class Player:
    class_counter = 0
    def __init__(self, color_location):
        self.id = Player.class_counter
        Player.class_counter += 1
        
        self.isactive = False
        self.name = ''
        self.color = color_location[0]
        self.cards = []
        self.location = color_location[1]
        self.home = color_location[1]
        self.current_card = False
        self.found_cards = []
        self.iscomputer = False
        
        self.player_images = {'yellow': 'player-yellow',
                              'blue': 'player-blue',
                              'green': 'player-green',
                              'red': 'player-red'}
    def __str__(self):
        return self.color
        
    def __hash__(self):
        return hash((self.id, self.isactive, self.name, self.color, self.location,
            self.home, self.current_card, tuple(self.cards), tuple(self.found_cards),
            self.iscomputer))
        
    def draw_card(self):
        """Update the current_card
        If replacing the current card, put the old card on the found_cards pile
        """
        if len(self.cards) != 0:
            if self.current_card:
                self.found_cards.append(self.current_card)
            self.current_card = self.cards.pop()
            return True
        else:
            self.current_card = None
            return False
            
    def current_card_found(self):
        """Item on current_card was found
        draw a new card
        """
        if self.draw_card() is False:
            return "winner"
        else:
            return None
        
    def remaining_cards(self):
        """Return string of remaining cards to find"""
        if self.current_card:
            i = 1
        else:
            i= 0
        return str(len(self.cards) + i)
