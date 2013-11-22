# coding: utf8

import unittest
import pickle
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
        self.assertEqual(-90, corner_tile.tile_image_rotation())

class TestGraph(unittest.TestCase):
    def setUp(self):
        _f = open("tests/testboard1.pickle")
        self.board = pickle.load(_f)
        _f.close()
        
        self.test_graph1 = Graph(self.board, (0,0))
        self.test_graph2 = Graph(self.board, (0,0))
        self.test_graph3 = Graph(self.board, (0,0))
        self.test_graph4 = Graph(self.board, (0,0))
        self.test_graph5 = Graph(self.board, (0,0))
        
    def test_path_connects(self):
        self.assertTrue(self.test_graph1.path_connects((0,0),(1,0),1))
        self.assertTrue(self.test_graph1.path_connects((1,0),(0,0),3))
        self.assertFalse(self.test_graph1.path_connects((0,0),(1,0),0))
        self.assertFalse(self.test_graph1.path_connects((0,0),(1,0),2))
        self.assertFalse(self.test_graph1.path_connects((3,4),(1,0),1))
        self.assertTrue(self.test_graph1.path_connects((4,4),(4,5),2))
        
    def test_find_adjacent_square(self):
        self.assertEqual(None, self.test_graph1.find_adjacent_square((0,0),0))
        self.assertEqual((1,0), self.test_graph1.find_adjacent_square((0,0),1))
        self.assertEqual((0,1), self.test_graph1.find_adjacent_square((0,0),2))
        self.assertEqual(None, self.test_graph1.find_adjacent_square((0,0),3))

suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayer)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestTile)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestGraph)
unittest.TextTestRunner(verbosity=2).run(suite)


