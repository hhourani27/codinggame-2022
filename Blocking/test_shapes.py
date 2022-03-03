import unittest
import numpy as np

from blocking_game import Shape

class TestShapes(unittest.TestCase):
    
    def test_no_duplicate_shape(self):
        shapes = Shape.get_all_shapes()
        
        s_A = {k:v for k,v in shapes.items() if k[0] == 'A'}
        self.assertListEqual(list(s_A.keys()), ['A001'])
        
        s_E = {k:v for k,v in shapes.items() if k[0] == 'E'}
        self.assertListEqual(list(s_E.keys()), ['E001','E002','E003','E004','E011','E012','E013','E014'])
        
        s_N = {k:v for k,v in shapes.items() if k[0] == 'N'}
        self.assertEqual(len(s_N),8*5)
        
        s_Q = {k:v for k,v in shapes.items() if k[0] == 'Q'}
        self.assertEqual(len(s_Q),4*5)
        
        s_U = {k:v for k,v in shapes.items() if k[0] == 'U'}
        self.assertEqual(len(s_U),1*5)
        
        s_H = {k:v for k,v in shapes.items() if k[0] == 'H'}
        self.assertEqual(len(s_H),1*4)
        
    def test_get_shapes(self):
        shapes = Shape.get_all_shapes(['A','B'])
        s_A = {k:v for k,v in shapes.items() if k[0] == 'A'}
        self.assertListEqual(list(shapes.keys()), ['A001','B001','B002','B011','B012'])
        
        


#%%
unittest.main()