class Board(dict):
    def __init__(self, *args, **kwargs ):
        dict.__init__(self, *args, **kwargs)
        
        self.current_tile = ''
        self.allowed_push_in_squares = ( (0,1),(0,3),(0,5),(1,0),(3,0),(5,0),
                                         (6,1),(6,3),(6,5),(1,6),(3,6),(5,6) )
        self.last_pushed_in = (0,0)             #update every move
        self.last_pushed_out = (0,0)             #update every move
        
    def push_in(self, push_in_square):
        """Push tile into push_square
        Update row values
        Update current_tile
        """
        if push_in_square not in self.allowed_push_in_squares:
            raise Exception
        row_lists = { (0, 1): [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
                      (0, 3): [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3)],
                      (0, 5): [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)],
                      (1, 0): [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)],
                      (3, 0): [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)],
                      (5, 0): [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)],
                      (6, 1): [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)],
                      (6, 3): [(6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3), (0, 3)],
                      (6, 5): [(6, 5), (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5)],
                      (1, 6): [(1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0)],
                      (3, 6): [(3, 6), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (3, 0)],
                      (5, 6): [(5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0)] }
        row_vals = row_lists[push_in_square]
        
        #update current_tile
        next_current_tile = self[row_vals[-1]]
        
        #push new tile in and push tiles along
        for i in reversed(xrange(1,7)):
            cur_square = row_vals[i]
            pre_square = row_vals[i-1]
            pre_tile = self[pre_square]
            self[cur_square] = pre_tile
        self[row_vals[0]] = self.current_tile
        self.current_tile = next_current_tile
        
        #Update last pushed in and out
        self.last_pushed_in = push_in_square
        self.last_pushed_out = row_lists[push_in_square][-1]
        
    def print_board(self):
        """Print text representation of the board"""
        keys = sorted(self.keys())
        i, j = (0,7)
        while j < 50:
            for key in keys[i:j]:
                print self[key],
            print
            i += 7; j += 7
        print
