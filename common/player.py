import random as rd
import sys
import traceback
import builtins as __builtin__

class PlayerKillException(Exception):
    pass

class Player:
    
    def __init__(self,id,inq,outq,attrs=None):
        self.id = id
        self.inq = inq
        self.outq = outq
        
        self.attrs = attrs
        
    def input(self):
        msg = self.inq.get()
        self.inq.task_done()
        
        # The simulator can send a kill signal to stop the player
        if msg is None:
            raise PlayerKillException()
        
        return msg
    
    def print(self, msg, file=None, flush=None):
        if file is not None:
            __builtin__.print(msg)
        else:
            self.outq.put(msg)
    
    def run(self):
        try:
            self.custom_code(self.input, self.print)
        except PlayerKillException:
            # A kill signal sent by the Simulator : stop the player
            pass
        except :
            # Another error raised by the player : log it
            __builtin__.print(traceback.format_exc())
    
    # Abstract method
    def custom_code(self, input, print):
        raise NotImplementedError("error message")

