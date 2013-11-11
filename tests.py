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

suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayer)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestTile)
unittest.TextTestRunner(verbosity=2).run(suite)
