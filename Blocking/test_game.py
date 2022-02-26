import unittest
import numpy as np

from blocking_game import BlockingGame as Game, Shape

class TestBlockingGame(unittest.TestCase):
    
    def play_game_1(self):
        N = 13
        board = np.full((N,N),'.')
        shapes = Shape.get_all_shapes_orientations()
        
        Game.place_shape_on_board(board, player_id=0, posx=0, posy=0, shape=shapes['D01'], n=3)
        Game.place_shape_on_board(board, player_id=1, posx=12, posy=12, shape=shapes['D02'], n=1)
        Game.place_shape_on_board(board, player_id=2, posx=12, posy=0, shape=shapes['S01'], n=5)
        Game.place_shape_on_board(board, player_id=0, posx=2, posy=2, shape=shapes['F13'], n=4)
        Game.place_shape_on_board(board, player_id=1, posx=10, posy=11, shape=shapes['S02'], n=1)
        Game.place_shape_on_board(board, player_id=2, posx=9, posy=3, shape=shapes['R11'], n=5)
        Game.place_shape_on_board(board, player_id=0, posx=4, posy=5, shape=shapes['R01'], n=4)
        Game.place_shape_on_board(board, player_id=1, posx=7, posy=8, shape=shapes['R01'], n=2)
        
        return board
    
    def test_corners_sides(self):
        N = 13
        board = np.arange(N*N).astype(str).reshape((N,N))
        
        # Center cells
        x,y = (5,5)
        corners = Game.get_corners(board, N, x,y)
        self.assertCountEqual(corners,['56','58','82','84'])
        sides = Game.get_sides(board, N, x, y)
        self.assertCountEqual(sides,['57','69','71','83'])
        
        # Corner cells
        x,y = (0,0)
        corners = Game.get_corners(board, N, x, y)
        self.assertCountEqual(corners,['14'])
        sides = Game.get_sides(board, N, x, y)
        self.assertCountEqual(sides,['1','13'])        
        
        x,y = (0,12)
        corners = Game.get_corners(board, N, x,y)
        self.assertCountEqual(corners,['24'])
        sides = Game.get_sides(board, N, x, y)
        self.assertCountEqual(sides,['11','25'])
        
        x,y = (12,12)
        corners = Game.get_corners(board, N, x,y)
        self.assertCountEqual(corners,['154'])
        sides = Game.get_sides(board, N, x, y)
        self.assertCountEqual(sides,['155','167'])
        
        # Side cells
        x,y = (0,1)
        corners = Game.get_corners(board, N, x,y)
        self.assertCountEqual(corners,['13','15'])
        sides = Game.get_sides(board, N, x, y)
        self.assertCountEqual(sides,['0','2','14'])
                
        x,y = (5,0)
        corners = Game.get_corners(board, N, x,y)
        self.assertCountEqual(corners,['53','79'])
        sides = Game.get_sides(board, N, x, y)
        self.assertCountEqual(sides,['52','66','78'])

        x,y = (5,12)
        corners = Game.get_corners(board, N, x,y)
        self.assertCountEqual(corners,['63','89'])
        sides = Game.get_sides(board, N, x, y)
        self.assertCountEqual(sides,['64','76','90'])        

    def test_well_connected_positions(self):
        N = 13
        board = np.full((N,N),'.')
        
        #Test first turns
        cps = Game.get_well_connected_positions(board, N, 0)
        self.assertCountEqual(cps,[(0,0)])
        
        board[0,0] = '0'
        cps = Game.get_well_connected_positions(board, N, 1)
        self.assertCountEqual(cps,[(12,12)])
        
        board[12,12] = '1'
        cps = Game.get_well_connected_positions(board, N, 2)
        self.assertCountEqual(cps,[(12,0)])
        
        board[12,0] = '2'
        cps = Game.get_well_connected_positions(board, N, 3)
        self.assertCountEqual(cps,[(0,12)])
        
        #Test next turns
        board = np.full((N,N),'.')
        board[0:2,0:2] = '0'
        board[11:13,11:13] = '1'
        cps = Game.get_well_connected_positions(board, N, 0)
        self.assertCountEqual(cps,[(2,2)])
        cps = Game.get_well_connected_positions(board, N, 1)
        self.assertCountEqual(cps,[(10,10)])
        
        board[[2,2,3],[2,3,2]] = '0'
        cps = Game.get_well_connected_positions(board, N, 0)
        self.assertCountEqual(cps,[(1,4),(3,4),(4,1),(4,3)])

        board[1:5,4] = '1'
        cps = Game.get_well_connected_positions(board, N, 0)
        self.assertCountEqual(cps,[(4,1),(4,3)])        

        board[4,0:4] = '1'
        cps = Game.get_well_connected_positions(board, N, 0)
        self.assertEqual(len(cps),0)          

    def test_place_shape_on_board(self):
        N = 13
        board_test = self.play_game_1()
        board_compare = np.full((N,N),'.')
        
        board_compare[[0,0,1],[0,1,1]] = '0'
        board_compare[[11,12,12],[12,11,12]] = '1'
        board_compare[[12,12,11,11,10],[0,1,1,2,2]] = '2'
        board_compare[[2,3,3,3],[2,2,3,4]] = '0'
        board_compare[[8,9,9,10,10],[9,9,10,10,11]] = '1'
        board_compare[[9,9,8,7,7],[3,4,4,4,5]] = '2'
        board_compare[[5,4,4,4,3],[5,5,6,7,7]] = '0'
        board_compare[[8,7,7,7,6],[6,6,7,8,8]] = '1'

        self.assertTrue((board_test==board_compare).all())
    
    def test_valid_moves_empty_board(self):
        N = 13
        board = np.full((N,N),'.')
        
        shapes = Shape.get_all_shapes_orientations()
        
        self.assertTrue(Game.is_valid_move(board, N, player_id=0, shape=shapes['O03'], posx=0, posy=0, n=3))
    
    def test_valid_moves(self):
        N = 13
        board = self.play_game_1()
        
        shapes = Shape.get_all_shapes_orientations()
        
        self.assertTrue(Game.is_valid_move(board, N, player_id=0, shape=shapes['H00'], posx=2, posy=8, n=3))
        self.assertTrue(Game.is_valid_move(board, N, player_id=0, shape=shapes['H00'], posx=2, posy=5, n=3))
        self.assertTrue(Game.is_valid_move(board, N, player_id=0, shape=shapes['D00'], posx=6, posy=4, n=2))
        self.assertTrue(Game.is_valid_move(board, N, player_id=0, shape=shapes['H00'], posx=5, posy=0, n=3))
        self.assertTrue(Game.is_valid_move(board, N, player_id=0, shape=shapes['H00'], posx=1, posy=3, n=3))

        self.assertFalse(Game.is_valid_move(board, N, player_id=0, shape=shapes['D00'], posx=6, posy=5, n=2),'Shape covers the side of the same player\'s shape')
        self.assertFalse(Game.is_valid_move(board, N, player_id=0, shape=shapes['C01'], posx=1, posy=3, n=3),'Shape goes outside board on the top')
        self.assertFalse(Game.is_valid_move(board, N, player_id=2, shape=shapes['H00'], posx=10, posy=0, n=4),'Shape goes outside board on the left side')
        self.assertFalse(Game.is_valid_move(board, N, player_id=0, shape=shapes['H00'], posx=6, posy=4, n=2),'Shape covers an opponent\'s shape')
        self.assertFalse(Game.is_valid_move(board, N, player_id=0, shape=shapes['H00'], posx=7, posy=0, n=3),'Shape is not placed in a connected cell')

        
        
        

        
        
#%%
unittest.main()
