import os
import json

class Data():
    
    def __init__(self):
        self.__data = None
    
    @property
    def data(self):
        return self.__data
    
    def load(self):
        with open(os.path.join("data", "data.json"), 'r') as f:
            self.__data = json.load(f)
    
    def dump(self):
        with open(os.path.join("data", "data.json"), 'w') as f:
            json.dump(self.__data, f, indent=4)
    
    def __getitem__(self, key):
        return self.__data[key]
    
    def __setitem__(self, key, value):
        self.__data[key] = value
        
d = Data()
d.load()