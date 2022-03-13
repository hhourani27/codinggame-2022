import unittest

from game_tic_tac_toe import TicTacToe

class TestTicTacToe(unittest.TestCase):
    
    def test_get_valid_moves(self):
        board = 0b000000000
        valid_moves = TicTacToe.get_valid_moves(board)
        
        self.assertCountEqual(valid_moves,
                              [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
                              )
        
        board = 0b100010001
        valid_moves = TicTacToe.get_valid_moves(board)
        
        self.assertCountEqual(valid_moves,
                              [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]
                              )
        
        board = 0b111111011
        valid_moves = TicTacToe.get_valid_moves(board)
        
        self.assertCountEqual(valid_moves,
                              [(2,0)]
                              )
        
        board = 0b111111111
        valid_moves = TicTacToe.get_valid_moves(board)
        
        self.assertCountEqual(valid_moves,
                              []
                              )
        
    def test_is_valid_moves(self):
        
        self.assertTrue(TicTacToe.is_valid_move(0b000000000, (0,0)))
        self.assertTrue(TicTacToe.is_valid_move(0b000000000, (0,2)))
        self.assertTrue(TicTacToe.is_valid_move(0b000000000, (1,1)))
        self.assertTrue(TicTacToe.is_valid_move(0b000000000, (2,0)))
        self.assertTrue(TicTacToe.is_valid_move(0b000000000, (2,2)))
        
        self.assertFalse(TicTacToe.is_valid_move(0b100010001, (0,0)))
        self.assertTrue(TicTacToe.is_valid_move(0b100010001, (0,2)))
        self.assertFalse(TicTacToe.is_valid_move(0b100010001, (1,1)))
        self.assertTrue(TicTacToe.is_valid_move(0b100010001, (2,0)))
        self.assertFalse(TicTacToe.is_valid_move(0b100010001, (2,2)))

        self.assertFalse(TicTacToe.is_valid_move(0b111111011, (0,0)))
        self.assertFalse(TicTacToe.is_valid_move(0b111111011, (0,2)))
        self.assertFalse(TicTacToe.is_valid_move(0b111111011, (1,1)))
        self.assertTrue(TicTacToe.is_valid_move(0b111111011, (2,0)))
        self.assertFalse(TicTacToe.is_valid_move(0b111111011, (2,2)))
        
        self.assertFalse(TicTacToe.is_valid_move(0b111111111, (0,0)))
        self.assertFalse(TicTacToe.is_valid_move(0b111111111, (0,2)))
        self.assertFalse(TicTacToe.is_valid_move(0b111111111, (1,1)))
        self.assertFalse(TicTacToe.is_valid_move(0b111111111, (2,0)))
        self.assertFalse(TicTacToe.is_valid_move(0b111111111, (2,2)))
        
    def test_place_move_on_board(self):
        self.assertEqual(TicTacToe.place_move_on_board(0b000000000, (0,0)),
                         0b100000000)
        self.assertEqual(TicTacToe.place_move_on_board(0b000000000, (0,2)),
                         0b001000000)
        self.assertEqual(TicTacToe.place_move_on_board(0b000000000, (1,1)),
                         0b000010000)
        self.assertEqual(TicTacToe.place_move_on_board(0b000000000, (2,0)),
                         0b000000100)
        self.assertEqual(TicTacToe.place_move_on_board(0b000000000, (2,2)),
                         0b000000001)
        
        self.assertEqual(TicTacToe.place_move_on_board(0b100010001, (0,2)),
                         0b101010001)
        self.assertEqual(TicTacToe.place_move_on_board(0b100010001, (2,0)),
                         0b100010101)

        self.assertEqual(TicTacToe.place_move_on_board(0b111111011, (2,0)),
                         0b111111111)
        
    def test_is_winner(self):
        self.assertTrue(TicTacToe.is_winner(0b111000000))
        self.assertTrue(TicTacToe.is_winner(0b000111000))
        self.assertTrue(TicTacToe.is_winner(0b000000111))
        self.assertTrue(TicTacToe.is_winner(0b100100100))
        self.assertTrue(TicTacToe.is_winner(0b010010010))
        self.assertTrue(TicTacToe.is_winner(0b001001001))
        self.assertTrue(TicTacToe.is_winner(0b100010001))
        self.assertTrue(TicTacToe.is_winner(0b001010100))
        
        self.assertTrue(TicTacToe.is_winner(0b111001000))
        self.assertTrue(TicTacToe.is_winner(0b010111000))
        self.assertTrue(TicTacToe.is_winner(0b000110111))
        self.assertTrue(TicTacToe.is_winner(0b111100100))
        self.assertTrue(TicTacToe.is_winner(0b010010011))
        self.assertTrue(TicTacToe.is_winner(0b001001011))
        self.assertTrue(TicTacToe.is_winner(0b101010001))
        self.assertTrue(TicTacToe.is_winner(0b101010100))
        
        self.assertFalse(TicTacToe.is_winner(0b000000000))
        self.assertFalse(TicTacToe.is_winner(0b101000000))
        self.assertFalse(TicTacToe.is_winner(0b100000100))
        self.assertFalse(TicTacToe.is_winner(0b001000100))
        self.assertFalse(TicTacToe.is_winner(0b100010000))
        self.assertFalse(TicTacToe.is_winner(0b001000001))
        
        self.assertFalse(TicTacToe.is_winner(0b101000101))
        self.assertFalse(TicTacToe.is_winner(0b010101010))
        self.assertFalse(TicTacToe.is_winner(0b110011100))
        self.assertFalse(TicTacToe.is_winner(0b101110010))
        
#%%
unittest.main()