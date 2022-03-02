import unittest
from blocking_game import MoveDatabase as md

class TestMovingDatabase(unittest.TestCase):
    
    def test_encode_move(self):
        move_idx,cell_idx = md.init_movedb(encode=False)
        
        for move in move_idx:
            move_enc = md.encode_move(move)
            move_dec = md.decode_move(move_enc)
            
            self.assertEqual(move,move_dec) 
            
    def test_encode_cell(self):
        move_idx,cell_idx = md.init_movedb(encode=False)
        
        for cell in cell_idx:
            cell_enc = md.encode_cell(cell)
            cell_dec = md.decode_cell(cell_enc)
            
            self.assertEqual(cell,cell_dec)
            
    def test_remove_letters(self):
        movedb = md()
        moves_A = [m for m in movedb.move_idx if md.decode_move(m)[2][0] == 'A']
        self.assertTrue(len(moves_A) > 0)
        
        movedb.remove_shape_letter('A')
        moves_A = [m for m in movedb.move_idx if md.decode_move(m)[2][0] == 'A']
        self.assertTrue(len(moves_A) == 0)
        
#%%
unittest.main()