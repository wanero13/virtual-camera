import numpy as np
import json as js

class Reader():
    def __init__(self):
        self.file = './input.txt'

    def readFile(self):
        with open(self.file) as f:
            self.data = js.load(f)

        return np.array(self.data['polygons'])