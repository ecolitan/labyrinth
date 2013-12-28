# coding: utf8

import unittest
import pickle
from player import Player
from tile import BoardTile
from graph import Graph
from labyrinth import NewGame
from board import Board

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.testPlayer1 = Player(('blue', (0,0)))

        _f = open("tests/testPlayer2.pickle")
        self.testPlayer2 = pickle.load(_f)
        _f.close()
        """
        isactive        True
        name            ''
        color           yellow
        cards           ['spider', 'dwarf', 'book', 'crown', 'mouse',
                        'lizzard', 'keys', 'bat', 'moth', 'beetle', 'map']
        location        (6, 6)
        home            (6, 6)
        current_card    fairy
        found_cards     []
        iscomputer      False
        __str__()       yellow
        __hash__()      5409634877126960526
        """
        
    def test_attributes(self):
        self.assertIs(type(self.testPlayer1.id), int)
        self.assertIs(type(self.testPlayer1.isactive), bool)
        self.assertIs(type(self.testPlayer1.name), str)
        self.assertIs(type(self.testPlayer1.color), str)
        self.assertFalse(self.testPlayer1.iscomputer)
        
    def test__str__(self):
        self.assertEqual('blue', self.testPlayer1.__str__())
        self.assertEqual('yellow', self.testPlayer2.__str__())
        
    def test__hash__(self):
        self.assertEqual(5409634877126960526, hash(self.testPlayer2))
        
    def test_draw_card(self):
        #Load test object again, because it will be modififed
        _f = open("tests/testPlayer2.pickle")
        testPlayer2 = pickle.load(_f)
        _f.close()
        #Draw two cards
        self.assertEqual('map', testPlayer2.draw_card())
        self.assertEqual('beetle', testPlayer2.draw_card())
        #Draw eight cards
        for i in xrange(0,8):
            testPlayer2.draw_card()
        #Draw remaining card
        self.assertNotEqual(None, testPlayer2.draw_card())
        #List now empty
        self.assertEqual(None, testPlayer2.draw_card())
        
    def test_current_card_found(self):
        #Load test object again, because it will be modififed
        _f = open("tests/testPlayer2.pickle")
        testPlayer2 = pickle.load(_f)
        _f.close()
        #Draw all cards
        for i in xrange(0,len(testPlayer2.cards)):
            self.assertIsNone(testPlayer2.current_card_found())
        #Draw from empty stack
        self.assertEqual("winner", testPlayer2.current_card_found())
        
    def test_remaining_cards(self):
        #Load test object again, because it will be modififed
        _f = open("tests/testPlayer2.pickle")
        testPlayer2 = pickle.load(_f)
        _f.close()
        self.assertEqual("12", testPlayer2.remaining_cards())
        testPlayer2.draw_card()
        self.assertEqual("11", testPlayer2.remaining_cards())
        
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
        
    def test__repr__(self):
        self.assertEqual(None, BoardTile(self.sample_exits1).__repr__())
        self.assertEqual('map', BoardTile(self.sample_exits1, 'map').__repr__())
        
    def test__str__(self):
        self.assertEqual('None', BoardTile(self.sample_exits1).__str__())
        self.assertEqual('map', BoardTile(self.sample_exits1, 'map').__str__())
        
    def test__hash__(self):
        tile1 = BoardTile([True,True,False,False])
        tile2 = BoardTile([True,True,False,False])
        tile3 = BoardTile([True,True,False,False])
        tile1.id = 0
        tile2.id = 0
        tile3.id = 0
        self.assertEqual(8411025243293485130, tile1.__hash__())
        self.assertEqual(8411025243293485130, hash(tile1))
        
        #~ self.assertEqual(271934571521961151, hash(self.tile2))
        
    def test__eq__(self):
        tile1 = BoardTile([True,True,False,False])
        tile2 = BoardTile([True,True,False,False], 'map')
        tile3 = BoardTile([True,True,False,False])
        tile1.id = 0
        tile2.id = 0
        tile3.id = 0
        self.assertNotEqual(tile1, tile2)
        self.assertEqual(tile1, tile3)
        
    def test__ne__(self):
        tile1 = BoardTile([True,True,False,False])
        tile2 = BoardTile([True,True,False,False], 'map')
        tile3 = BoardTile([True,True,False,False])
        tile1.id = 0
        tile2.id = 0
        tile3.id = 0
        self.assertNotEqual(tile1, tile2)
        self.assertEqual(tile1, tile3)
        
    def test_rotate(self):
        sample1_rotations = [ [False,True,True,False],  #90
                              [False,False,True,True],  #180
                              [True,False,False,True],  #270
                              [True,True,False,False] ] #360
        
        test_tile = BoardTile(self.sample_exits1)
        for rotation in sample1_rotations:
            test_tile.rotate()
            self.assertEqual(rotation, test_tile.exits)
            
    def test_rotate_n_times(self):
        tile1 = BoardTile([True,True,False,False])
        with self.assertRaises(Exception):
            tile1.rotate_n_times(4)
            tile1.rotate_n_times(-1)
        sample1_rotations = [ [False,True,True,False],  #90
                              [False,False,True,True],  #180
                              [True,False,False,True],  #270
                              [True,True,False,False] ] #360
        for i in xrange(0,4):
            test_tile = BoardTile([True,True,False,False])
            test_tile.rotate_n_times(i)
            self.assertEqual(sample1_rotations[i], test_tile.exits)
            #TODO
        
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
        
        self.test_graph_obj1 = Graph(self.board, (0,0))
        self.test_graph_obj2 = Graph(self.board, (0,3))
        self.test_graph_obj3 = Graph(self.board, (2,1))
        self.test_graph1 = {(0,0): [(1,0)],
                            (1,0): [(2,0), (1,1)] }
        self.test_graph2 = {(0,3): [(1,3), (0,4)],
                            (1,3): [(1,4)],
                            (0,4): [(0,5)],
                            (0,5): [(1,5)] }
        self.test_graph3 = {}
        
    def test_path_connects(self):
        self.assertTrue(self.test_graph_obj1.path_connects((0,0),(1,0),1))
        self.assertTrue(self.test_graph_obj1.path_connects((1,0),(0,0),3))
        self.assertFalse(self.test_graph_obj1.path_connects((0,0),(1,0),0))
        self.assertFalse(self.test_graph_obj1.path_connects((0,0),(1,0),2))
        self.assertFalse(self.test_graph_obj1.path_connects((3,4),(1,0),1))
        self.assertTrue(self.test_graph_obj1.path_connects((4,4),(4,5),2))
        self.assertFalse(self.test_graph_obj3.path_connects((2,1),(2,2),2))
        
    def test_find_adjacent_square(self):
        self.assertEqual(None, self.test_graph_obj1.find_adjacent_square((0,0),0))
        self.assertEqual((1,0), self.test_graph_obj1.find_adjacent_square((0,0),1))
        self.assertEqual((0,1), self.test_graph_obj1.find_adjacent_square((0,0),2))
        self.assertEqual(None, self.test_graph_obj1.find_adjacent_square((0,0),3))
        self.assertEqual((2,2), self.test_graph_obj3.find_adjacent_square((2,1),2))
        
    def test_square_in_graph_index(self):
        self.assertTrue(self.test_graph_obj1.square_in_graph_index((0,0), graph=self.test_graph1))
        self.assertFalse(self.test_graph_obj1.square_in_graph_index((0,6), graph=self.test_graph1))
        self.assertTrue(self.test_graph_obj1.square_in_graph_index((0,4), graph=self.test_graph2))
        self.assertFalse(self.test_graph_obj1.square_in_graph_index((0,1), graph=self.test_graph2))
        self.assertFalse(self.test_graph_obj3.square_in_graph_index((2,2), graph=self.test_graph3))
        
    def test_square_in_graph_node(self):
        self.assertFalse(self.test_graph_obj1.square_in_graph_node((6,6), graph=self.test_graph1))
        self.assertFalse(self.test_graph_obj1.square_in_graph_node((0,0), graph=self.test_graph1))
        self.assertTrue(self.test_graph_obj1.square_in_graph_node((1,0), graph=self.test_graph1))
        self.assertTrue(self.test_graph_obj1.square_in_graph_node((1,1), graph=self.test_graph1))
        
    #~ def test_build_graph(self):
        #~ self.assertEqual(self.test_graph1, self.test_graph_obj1.graph)
        #~ self.assertEqual(self.test_graph3, self.test_graph_obj3.graph)
        
        #~ self.assertEqual(self.test_graph2, self.test_graph_obj2.graph)
        # Not sure how to write this test, need a way to test if two graphs which
        # have different orders are actually equivalent 
        
    def test_travel_between_in_graph(self):
        self.assertTrue(self.test_graph_obj1.travel_between_in_graph((0,0), (1,1) ,graph=self.test_graph1))
        self.assertFalse(self.test_graph_obj1.travel_between_in_graph((0,0), (4,4) ,graph=self.test_graph1))
        self.assertTrue(self.test_graph_obj2.travel_between_in_graph((1,3), (1,5) ,graph=self.test_graph2))
        self.assertFalse(self.test_graph_obj2.travel_between_in_graph((0,0), (4,4) ,graph=self.test_graph2))
        self.assertFalse(self.test_graph_obj2.travel_between_in_graph((0,0), (4,4) ,graph=self.test_graph1))
        
class TestNewGame(unittest.TestCase):
    def setUp(self):
        _f = open("tests/testboard1.pickle")
        self.board = pickle.load(_f)
        _f.close()
        
        self.test_game_obj1 = Graph(self.board, (0,0))
        self.test_graph_obj2 = Graph(self.board, (0,3))
        self.test_graph1 = {(0,0): [(1,0)],
                            (1,0): [(2,0), (1,1)] }
        self.test_graph2 = {(0,3): [(1,3), (0,4)],
                            (1,3): [(1,4)],
                            (0,4): [(0,5)],
                            (0,5): [(1,5)] }
                            
    def test_mouse_over_board(self):
        self.assertEqual((0,0), NewGame(cli=True).mouse_over_board((359, 171)))
        self.assertEqual((4,4), NewGame(cli=True).mouse_over_board((719, 545)))
        self.assertEqual((0,6), NewGame(cli=True).mouse_over_board((374, 729)))
        self.assertEqual((6,1), NewGame(cli=True).mouse_over_board((932, 268)))
        self.assertEqual((6,4), NewGame(cli=True).mouse_over_board((936, 540)))
        self.assertFalse(NewGame(cli=True).mouse_over_board((244, 57)))
        self.assertFalse(NewGame(cli=True).mouse_over_board((127, 642)))
        self.assertFalse(NewGame(cli=True).mouse_over_board((404, 864)))
        self.assertFalse(NewGame(cli=True).mouse_over_board((1024, 569)))
        self.assertFalse(NewGame(cli=True).mouse_over_board((1013, 23)))
        
    def test_load_images(self):
        pass




        
        

    
suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayer)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestTile)
unittest.TextTestRunner(verbosity=2).run(suite)
#~ 
#~ suite = unittest.TestLoader().loadTestsFromTestCase(TestGraph)
#~ unittest.TextTestRunner(verbosity=2).run(suite)
#~ 
#~ suite = unittest.TestLoader().loadTestsFromTestCase(TestNewGame)
#~ unittest.TextTestRunner(verbosity=2).run(suite)


