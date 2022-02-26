import random as rd
import sys
import builtins as __builtin__

class Player:
    
    def __init__(self,id,inq,outq):
        self.id = id
        self.inq = inq
        self.outq = outq
        
        
    def input(self):
        msg = self.inq.get()
        self.inq.task_done()
        
        # Detect a kill signal
        if msg is None:
            raise Exception('Stop player thread')
        
        return msg
    
    def print(self,msg,file=None):
        if file is not None:
            __builtin__.print(msg)
        else:
            self.outq.put(msg)
    
    def run(self):
        try:
            self.custom_code(self.input, self.print)
        except Exception as e:
            pass
    
    # Abstract method
    def custom_code(self, input, print):
        raise NotImplementedError("error message")

