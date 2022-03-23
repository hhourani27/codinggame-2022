from time import time
import timeit
import numpy as np
#%%
def is_won_1(p_board_bin):
    winning_configurations = [
        0b111000000,
        0b000111000,
        0b000000111,
        0b100100100,
        0b010010010,
        0b001001001,
        0b100010001,
        0b001010100
        ]
    
    for conf in winning_configurations:
        if conf == conf & p_board_bin:
            return True
        
    return False

def is_won_2(p_board_bin):
    winning_configurations = (
        0b111000000,
        0b000111000,
        0b000000111,
        0b100100100,
        0b010010010,
        0b001001001,
        0b100010001,
        0b001010100
        )
    
    for conf in winning_configurations:
        if conf == conf & p_board_bin:
            return True
        
    return False

def is_won_3(p_board_bin):
    winning_configurations = {
        0b111000000,
        0b000111000,
        0b000000111,
        0b100100100,
        0b010010010,
        0b001001001,
        0b100010001,
        0b001010100
        }
    
    for conf in winning_configurations:
        if conf == conf & p_board_bin:
            return True
        
    return False


winning_configurations_list = [
    0b111000000,
    0b000111000,
    0b000000111,
    0b100100100,
    0b010010010,
    0b001001001,
    0b100010001,
    0b001010100
    ]

winning_configurations_tuple = (
    0b111000000,
    0b000111000,
    0b000000111,
    0b100100100,
    0b010010010,
    0b001001001,
    0b100010001,
    0b001010100
    )

winning_configurations_set = {
    0b111000000,
    0b000111000,
    0b000000111,
    0b100100100,
    0b010010010,
    0b001001001,
    0b100010001,
    0b001010100
    }

def is_won_4(p_board_bin):    
    for conf in winning_configurations_list:
        if conf == conf & p_board_bin:
            return True
        
    return False

def is_won_5(p_board_bin):    
    for conf in winning_configurations_tuple:
        if conf == conf & p_board_bin:
            return True
        
    return False

def is_won_5(p_board_bin):    
    for conf in winning_configurations_set:
        if conf == conf & p_board_bin:
            return True
        
    return False

#%%
N = 10000
timeit.timeit('is_won_1(0b001001001)', number=N)
timeit.timeit('is_won_2(0b001001001)', number=N)
timeit.timeit('is_won_3(0b001001001)', number=N)
timeit.timeit('is_won_4(0b001001001)', number=N)
timeit.timeit('is_won_5(0b001001001)', number=N)
timeit.timeit('is_won_6(0b001001001)', number=N)