from back.files import Reader
import numpy as np
import math


class Rotate:
    def __init__(self):
        self.reader = Reader()
        self.data = self.reader.readFile()

    def translate(self, tx, ty, tz):
        m = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])
        self.recalc(m)

    def horizontal(self,x):
        m = np.array([
            [math.cos(x), 0, math.sin(x), 0],
            [0, 1, 0, 0],
            [-1 * math.sin(x), 0, math.cos(x), 0],
            [0, 0, 0, 1]])
        self.recalc(m)

    def vertical(self, x):
        m = np.array([
            [1, 0, 0, 0],
            [0, math.cos(x), -1 * math.sin(x), 0],
            [0, math.sin(x), math.cos(x), 0],
            [0, 0, 0, 1]])
        self.recalc(m)

    def twist(self, x):
        m = np.array([
            [math.cos(x), -1 * math.sin(x), 0, 0],
            [math.sin(x), math.cos(x), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
        self.recalc(m)



    def recalc(self, m):
        a, b, c = self.data.shape
        figures = np.ndarray((a, b, c))
        for i in range(a):
            for j in range(b):
                old = np.array([
                    [self.data[i][j][0]],
                    [self.data[i][j][1]],
                    [self.data[i][j][2]],
                    [1]
                ])
                new = np.matmul(m, old)
                new = np.delete(new, 3)
                figures[i][j][0] = new[0]
                figures[i][j][1] = new[1]
                figures[i][j][2] = new[2]
        self.data = figures
