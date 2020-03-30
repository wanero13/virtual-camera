from back.rotations import Rotate
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPointF
import numpy
import math


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = 1280
        self.h = 720
        self.d = 400
        self.zstep = 20
        self.tstep = 5
        self.astep = float(math.pi / 18.0)
        self.rotate = Rotate()
        self.setGeometry(0, 0, self.w, self.h)
        self.setWindowTitle("Wirtualna Kamera")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.rotate.translate(0, 0, 60)

    def paintEvent(self, e):
        self.painter = QPainter(self)
        self.painter.translate(self.w / 2, self.h / 2)
        self.painter.scale(1, -1)
        self.painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        self.paint()
        self.painter.end()

    def keyPressEvent(self, e):
        key = e.key()
        # forward
        if key == Qt.Key_S:
            self.rotate.translate(0, 0, 1 * self.tstep)
        # backward
        elif key == Qt.Key_W:
            self.rotate.translate(0, 0, -1 * self.tstep)
        # left
        elif key == Qt.Key_D:
            self.rotate.translate(-1 * self.tstep, 0, 0)
        # right
        elif key == Qt.Key_A:
            self.rotate.translate(1 * self.tstep, 0, 0)
        # up
        elif key == Qt.Key_R:
            self.rotate.translate(0, 1 * self.tstep, 0)
        # down
        elif key == Qt.Key_T:
            self.rotate.translate(0, -1 * self.tstep, 0)
        # rotate left
        elif key == Qt.Key_Q:
            self.rotate.horizontal(self.astep)
        # rotate right
        elif key == Qt.Key_E:
            self.rotate.horizontal(-1 * self.astep)
        # rotate up
        elif key == Qt.Key_Z:
            self.rotate.vertical(self.astep)
        # rotate down
        elif key == Qt.Key_X:
            self.rotate.vertical(-1 * self.astep)
        # twist left
        elif key == Qt.Key_B:
            self.rotate.twist(self.astep)
        # twist right
        elif key == Qt.Key_N:
            self.rotate.twist(-1 * self.astep)
        # zoom in
        elif key == Qt.Key_C:
            self.zoom(self.zstep)
        # zoom out
        elif key == Qt.Key_V:
            self.zoom(-1 * self.zstep)
        e.accept()
        self.repaint()

    def zoom(self, x):
        self.d = self.d + x
        if self.d<0:
            self.d=0.000001

    def recalculate(self, point):
        x = point[0]
        y = point[1]
        z = point[2]
        if z <= 0:
            z = 0.000000001
        tempx = x * (self.d / z)
        tempy = y * (self.d / z)
        return tempx, tempy

    def paint(self):
        figures = self.rotate.data
        for figure in figures:
            points = []
            nodraw = []
            for point in figure:
                if point[2] < 0:
                    nodraw.append(1)
                else:
                    nodraw.append(0)
                x, y = self.recalculate(point)
                points.append(QPointF(x, y))
            for i in range(3):
                if nodraw[i] != 1 or nodraw[i + 1] != 1:
                    self.painter.drawLine(points[i], points[i + 1])
                if nodraw[i] != 1 or nodraw[i + 4] != 1:
                    self.painter.drawLine(points[i], points[i + 4])
            if nodraw[0] != 1 or nodraw[3] != 1:
                self.painter.drawLine(points[0], points[3])
            if nodraw[3] != 1 or nodraw[7] != 1:
                self.painter.drawLine(points[3], points[7])
            for i in range(4, 7):
                if nodraw[i] != 1 or nodraw[i + 1] != 1:
                    self.painter.drawLine(points[i], points[i + 1])
            if nodraw[4] != 1 or nodraw[7] != 1:
                self.painter.drawLine(points[4], points[7])
