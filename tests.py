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
        pass
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


suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayer)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestTile)
unittest.TextTestRunner(verbosity=2).run(suite)


