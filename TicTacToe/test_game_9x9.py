import unittest
import numpy as np


from game_tic_tac_toe_9x9 import TicTacToe

class TestTicTacToe(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None
    
    def test_slice_square(self):
        board = np.full((9,9),'0')
        board[4,4] = '1'
        
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        self.assertEqual(TicTacToe.slice_square(board_bin, (1,1)), 0b000010000)
        self.assertEqual(TicTacToe.slice_square(board_bin, (0,1)), 0b000000000)
        
        board[3,4] = '1'
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        self.assertEqual(TicTacToe.slice_square(board_bin, (1,1)), 0b010010000)
        
        board[5,4] = '1'
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        self.assertEqual(TicTacToe.slice_square(board_bin, (1,1)), 0b010010010)
        
        board[4,5] = '1'
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        self.assertEqual(TicTacToe.slice_square(board_bin, (1,1)), 0b010011010)
        
        board[4,0] = '1'
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        self.assertEqual(TicTacToe.slice_square(board_bin, (1,1)), 0b010011010)
        self.assertEqual(TicTacToe.slice_square(board_bin, (1,0)), 0b000100000)

        board[8,8] = '1'
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        self.assertEqual(TicTacToe.slice_square(board_bin, (2,2)), 0b000000001)
        
        #
        board = np.full((9,9),'0')
        board[5,7] = '1'
        board[6,4] = '1'
        board[2,5] = '1'
        board[8,7] = '1'
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        self.assertEqual(TicTacToe.slice_square(board_bin, (2,1)), 0b010000000)

        
    def test_cell9x9_to_cell3x3(self):
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(0,0),
                         (0,0))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(0,4),
                         (0,1))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(0,8),
                         (0,2))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(2,6),
                         (2,0))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(4,1),
                         (1,1))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(5,3),
                         (2,0))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(6,8),
                         (0,2))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(7,0),
                         (1,0))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(7,6),
                         (1,0))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(8,0),
                         (2,0))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(8,3),
                         (2,0))
        self.assertEqual(TicTacToe.cell9x9_to_cell3x3(8,8),
                         (2,2))
        
    def test_cell3x3_to_cell9x9(self):
        self.assertEqual(TicTacToe.cell3x3_to_cell9x9((0,0),(0,0)),
                         (0,0))
        self.assertEqual(TicTacToe.cell3x3_to_cell9x9((1,2),(0,0)),
                         (1,2))
        self.assertEqual(TicTacToe.cell3x3_to_cell9x9((0,2),(0,2)),
                         (0,8))
        self.assertEqual(TicTacToe.cell3x3_to_cell9x9((1,0),(1,0)),
                         (4,0))
        self.assertEqual(TicTacToe.cell3x3_to_cell9x9((1,1),(1,1)),
                         (4,4))
        self.assertEqual(TicTacToe.cell3x3_to_cell9x9((2,1),(1,2)),
                         (5,7))
        self.assertEqual(TicTacToe.cell3x3_to_cell9x9((2,1),(2,0)),
                         (8,1))
        self.assertEqual(TicTacToe.cell3x3_to_cell9x9((2,2),(2,2)),
                         (8,8))

    def test_get_valid_moves_9x9(self):    
        board = np.full((9,9),'0')
        all_moves = [(r,c) for r in range(9) for c in range(9)]        
        
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, (-1,-1))
        self.assertCountEqual(valid_moves, 
                              all_moves
                              )
        ##
        board[5,7] = '1'
        board[6,4] = '1'
        last_move = (6,4)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(2,3),(2,5),(2,4),(0,3),(0,4),(1,3),(0,5),(1,5),(1,4)]
                              )
        ##
        board[2,5] = '1'
        board[8,7] = '1'
        last_move = (8,7)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(8,5),(7,3),(7,5),(6,5),(7,4),(6,3),(8,3),(8,4)]
                              )
        ##
        board[8,4] = '1'
        board[7,4] = '1'
        last_move = (7,4)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(4,3),(4,4),(5,5),(5,3),(3,3),(3,4),(5,4),(4,5),(3,5)]
                              )
        ##
        board[4,5] = '1'
        board[3,8] = '1'
        last_move = (3,8)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(1,8),(0,7),(2,6),(2,8),(1,7),(1,6),(2,7),(0,6),(0,8)]
                              )
        ##
        board[1,8] = '1'
        board[3,7] = '1'
        last_move = (3,7)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(1,3),(2,3),(0,5),(1,5),(0,4),(2,4),(0,3),(1,4)]
                              )        
        ##
        board[0,3] = '1'
        board[2,1] = '1'
        last_move = (2,1)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(8,5),(7,3),(6,3),(8,3),(6,5),(7,5)]
                              )     
        ##
        board[7,3] = '1'
        board[3,1] = '1'
        last_move = (3,1)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(0,5),(0,4),(2,4),(2,3),(1,5),(1,3),(1,4)]
                              )    
        ##
        board[0,4] = '1'
        board[0,5] = '1'
        last_move = (0,5)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(1,6),(0,8),(0,7),(2,7),(1,7),(2,8),(0,6),(2,6)]
                              )    
        ##
        board[2,6] = '1'
        board[7,1] = '1'
        last_move = (7,1)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(4,4),(3,4),(5,4),(3,3),(3,5),(4,3),(5,5),(5,3)]
                              )    
        ##
        board[4,4] = '1'
        board[3,4] = '1'
        last_move = (3,4)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(2,4),(1,4),(1,5),(1,3),(2,3)]
                              )    
        ##
        board[2,4] = '1'
        board[6,3] = '1'
        last_move = (6,3)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(0,0),(2,0),(0,1),(1,1),(0,2),(1,0),(2,2),(1,2)]
                              )    
        ##
        board[1,1] = '1'
        board[3,5] = '1'
        last_move = (3,5)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(0,8),(1,6),(1,7),(2,8),(2,7),(0,7),(0,6)]
                              )    
        ##
        board[0,8] = '1'
        board[1,6] = '1'
        last_move = (1,6)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(4,1),(5,0),(4,0),(3,2),(3,0),(5,1),(4,2),(5,2)]
                              )    
        ##
        board[5,0] = '1'
        board[6,1] = '1'
        last_move = (6,1)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b000000000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(2,3),(1,4),(1,5),(1,3)]
                              )    
        ##
        board[1,4] = '1'
        board[3,3] = '1'
        last_move = (3,3)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b010010000, last_move)
        self.assertCountEqual(valid_moves, 
                              [(0,0),(0,1),(1,2),(0,2),(1,0),(2,0),(2,2)]
                              )    
        ##
        board[0,1] = '1'
        board[8,1] = '1'
        last_move = (8,1)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b010010100, last_move)
        self.assertCountEqual(valid_moves, 
                              [(6,5),(7,5),(8,3),(8,5)]
                              )    
        ##
        board[6,5] = '1'
        board[1,7] = '1'
        last_move = (1,7)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b010010100, last_move)
        self.assertCountEqual(valid_moves, 
                              [(5,6),(2,2),(5,8),(7,7),(0,2),(4,7),(7,5),(5,2),(2,0),(0,7),(0,6),(6,8),(3,6),(4,1),(6,6),(2,8),(3,2),(7,6),(3,0),(8,3),(8,6),(4,2),(8,8),(2,7),(4,0),(1,2),(5,1),(7,8),(1,0),(0,0),(6,7),(8,5),(4,6),(4,8)]
                              )    
        ##
        board[8,5] = '1'
        board[6,7] = '1'
        last_move = (6,7)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b010010100, last_move)
        self.assertCountEqual(valid_moves, 
                              [(7,5),(0,7),(2,0),(3,6),(7,8),(8,3),(3,0),(1,0),(2,7),(1,2),(5,8),(2,2),(4,7),(7,6),(8,6),(2,8),(0,0),(6,6),(5,6),(4,1),(0,6),(8,8),(0,2),(6,8),(4,8),(4,0),(7,7),(5,2),(3,2),(4,6),(5,1),(4,2)]
                              )    
        ##
        board[5,8] = '1'
        board[7,7] = '1'
        last_move = (7,7)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b010010101, last_move)
        self.assertCountEqual(valid_moves, 
                              [(4,1),(0,0),(2,2),(0,7),(4,8),(0,6),(5,2),(7,5),(0,2),(4,7),(2,0),(5,6),(3,2),(5,1),(4,6),(3,0),(4,2),(2,8),(1,0),(4,0),(1,2),(2,7),(8,3),(3,6)]
                              )    
        ##
        board[4,1] = '1'
        board[3,6] = '1'
        last_move = (3,6)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b010011101, last_move)
        self.assertCountEqual(valid_moves, 
                              [(2,0),(0,2),(1,2),(1,0),(2,2),(0,0)]
                              )    
        ##
        board[1,0] = '1'
        board[3,2] = '1'
        last_move = (3,2)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b010011101, last_move)
        self.assertCountEqual(valid_moves, 
                              [(2,8),(0,6),(0,7),(2,7)]
                              )    

    def test_get_valid_moves_9x9_2(self):    
        board = np.full((9,9),'0')
        all_moves = [(r,c) for r in range(9) for c in range(9)]
        
        board[0:3,0:3] = '1'
        board[3,3] = '1'
        last_move = (3,3)
        board_bin = TestTicTacToe.board_2Darray_to_binary(board)
        expected_valid_moves = list(
            set(all_moves) - set([(r,c) for r in range(3) for c in range(3)]) -set([(3,3)])
            )
 
        
        valid_moves = TicTacToe.get_valid_moves_9x9(board_bin, 0b100000000, last_move)
        
        
        self.assertCountEqual(valid_moves, expected_valid_moves)    

    def test_place_move_on_board(self):
        board = 0b000000000000000000000000000000000000000000000000000000000000000000000000000000000
        
        board2 = TicTacToe.place_move_on_board(board, (0,1))
        expected_board2 = 0b010000000000000000000000000000000000000000000000000000000000000000000000000000000
        
        self.assertEqual(board2, expected_board2)
        
        board3 = TicTacToe.place_move_on_board(board2, (8,8))
        expected_board3 = 0b010000000000000000000000000000000000000000000000000000000000000000000000000000001

        self.assertEqual(board3, expected_board3)

    def test_set_bin(self):
        self.assertEqual(TicTacToe.set_bit(0b000000000, 0, 0), 0b100000000)
        self.assertEqual(TicTacToe.set_bit(0b000000000, 1, 1), 0b000010000)
        self.assertEqual(TicTacToe.set_bit(0b000000000, 2, 2), 0b000000001)
        self.assertEqual(TicTacToe.set_bit(0b100100100, 0, 2), 0b101100100)
        self.assertEqual(TicTacToe.set_bit(0b100000100, 1, 0), 0b100100100)

        
#%%    

    def board_2Darray_to_binary(board):
        board_str = ''.join(board.flatten())
        return int(board_str,2)
                
#%%
unittest.main()

#%%
