class Board(dict):
    def __init__(self, *args, **kwargs ):
        dict.__init__(self, *args, **kwargs)
        
        self.current_tile = ''
