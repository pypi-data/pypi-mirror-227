# -*- coding: utf-8 -*-

class DBR():
    def __init__(self, *args, **kwargs):
        self.unpack(**kwargs)
        self.records = list(args) or []
    
    def unpack(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)
    
    
    def __len__(self):
        return len(self.records)
    
    
    def __in__(self, value):
        return value in self.records
    
    
    def __getitem__(self, ix):
        return self.records[ix]
    
    
    def __setitem__(self, ix, value):
        self.records[ix] = value  
        
        
    def __repr__(self):
        return f"<DB Response ({len(self)} Records)>"