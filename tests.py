# coding: utf8

import unittest
from player import Player
from tile import BoardTile
from graph import Graph
from labyrinth import NewGame

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_attributes(self):
        self.assertIs(type(Player().id), int)
        self.assertIs(type(Player().isactive), bool)
        self.assertIs(type(Player().name), str)
        self.assertIs(type(Player().color), str)
        
class TestTile(unittest.TestCase):
    def setUp(self):
        self.sample_exits1 = [True,True,False,False]
        self.sample_exits2 = [True,False,True,False]
        self.sample_exits3 = [True,True,True,False]
        
    def test_attributes(self):
        self.assertIs(type(BoardTile(self.sample_exits1).id), int)
        self.assertIs(type(BoardTile(self.sample_exits1,'').item), str)
        self.assertIs(type(BoardTile(self.sample_exits1,'','').action), str)
        self.assertEqual(self.sample_exits1, BoardTile(self.sample_exits1).exits)
        
    def test_rotate(self):
        sample1_rotations = [ [False,True,True,False],  #90
                              [False,False,True,True],  #180
                              [True,False,False,True],  #270
                              [True,True,False,False] ] #360
        
        test_tile = BoardTile(self.sample_exits1)
        for rotation in sample1_rotations:
            test_tile.rotate()
            self.assertEqual(rotation, test_tile.exits)
        
    def test_randomise_orientation(self):
        rotation_counter = { str([False,True,True,False]):0.0,
                             str([False,False,True,True]):0.0,
                             str([True,False,False,True]):0.0,
                             str([True,True,False,False]):0.0 }
        test_tile = BoardTile(self.sample_exits1)
        num_trials = 100000
        for i in xrange(0,num_trials):
            test_tile.randomise_orientation()
            rotation_counter[str(test_tile.exits)] += 1
        counts = rotation_counter.values()
        mean = sum(counts)/len(counts)
        std_deviation = (sum([j**2 for j in [i - mean for i in counts]])/len(counts))**0.5
        p = std_deviation/num_trials
        self.assertTrue(p<0.05, 'p value was ' + str(p))
        
    def test_determine_tile_type(self):
        self.assertEqual('corner', BoardTile([True,True,False,False]).determine_tile_type())
        self.assertEqual('straight', BoardTile([False,True,False,True]).determine_tile_type())
        self.assertEqual('tee', BoardTile([True,True,True,False]).determine_tile_type())
        
    def test_tile_image_rotation(self):
        corner_tile = BoardTile([True,True,False,False])
        self.assertEqual(0, corner_tile.tile_image_rotation())
        corner_tile.rotate()
        self.assertEqual(90, corner_tile.tile_image_rotation())

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.board = {}
        movable_squares = ((1, 3), (3, 0), (3, 2), (2, 1), (5, 6), (1, 6),
                           (5, 1), (2, 5), (0, 3), (1, 2), (5, 5), (6, 3),
                           (1, 5), (5, 0), (3, 5), (4, 1), (1, 1), (5, 4),
                           (3, 6), (4, 5), (1, 4), (2, 3), (1, 0), (6, 5),
                           (3, 3), (0, 1), (5, 3), (3, 4), (6, 1), (3, 1),
                           (4, 3), (0, 5), (5, 2))
        self.board[(0,0)] = BoardTile([False,True,True,False])
        self.board[(0,6)] = BoardTile([False,False,True,True])
        self.board[(6,6)] = BoardTile([True,False,False,True])
        self.board[(6,0)] = BoardTile([True,True,False,False])
        self.board[(0,2)] = BoardTile([False,True,True,True])
        self.board[(0,4)] = BoardTile([False,True,True,True])
        self.board[(2,6)] = BoardTile([True,False,True,True])
        self.board[(4,6)] = BoardTile([True,False,True,True])
        self.board[(6,4)] = BoardTile([True,True,False,True])
        self.board[(6,2)] = BoardTile([True,True,False,True])
        self.board[(2,0)] = BoardTile([True,True,True,False])
        self.board[(4,0)] = BoardTile([True,True,True,False])
        self.board[(2,2)] = BoardTile([False,True,True,True])
        self.board[(4,2)] = BoardTile([False,True,True,True])
        self.board[(2,4)] = BoardTile([False,True,True,True])
        self.board[(4,4)] = BoardTile([False,True,True,True])
        tiles = []
        for i in xrange(0,6):
            tiles.append(BoardTile([False,True,True,True]))
        for i in xrange(0,6):
            tiles.append(BoardTile([False,True,False,True]))
        for i in xrange(0,6):
            tiles.append(BoardTile([False,True,False,True]))
        for i in xrange(0,6):
            tiles.append(BoardTile([True,True,False,False]))
        for i in xrange(0,4):
            tiles.append(BoardTile([True,True,False,False]))
        for i in xrange(0,6):
            tiles.append(BoardTile([True,True,False,False]))
        
        for square in self.movable_squares:
            self.board[square] = tiles.pop()

        
        
        
        

suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayer)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestTile)
unittest.TextTestRunner(verbosity=2).run(suite)


