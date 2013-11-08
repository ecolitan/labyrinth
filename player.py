class Player:
    class_counter = 0
    def __init__(self):
        self.id = Player.class_counter
        Player.class_counter += 1
        
        self.isactive = False
        self.name = ''
        self.color = ''
        
    def __str__(self):
        return self.name
