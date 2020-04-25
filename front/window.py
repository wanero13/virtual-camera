from back.rotations import Rotate
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QPen, QPolygonF, QBrush
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
        self.colors = [Qt.gray, Qt.yellow, Qt.blue, Qt.green, Qt.white, Qt.cyan]
        self.colorCheck = 0

    def paintEvent(self, e):
        self.painter = QPainter(self)
        self.painter.translate(self.w / 2, self.h / 2)
        self.painter.scale(1, -1)
        self.painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        self.painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
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
        if self.d < 0:
            self.d = 0.000001

    def recalculate(self, point):
        x = point[0]
        y = point[1]
        z = point[2]
        if z <= 0:
            z = 0.000000001
        tempx = x * (self.d / z)
        tempy = y * (self.d / z)
        return tempx, tempy

    # def paint(self):
    #     figures = self.rotate.data
    #     for figure in figures:
    #         points = []
    #         nodraw = []
    #         for point in figure:
    #             if point[2] < 0:
    #                 nodraw.append(1)
    #             else:
    #                 nodraw.append(0)
    #             x, y = self.recalculate(point)
    #             points.append(QPointF(x, y))
    #         for i in range(3):
    #             if nodraw[i] != 1 or nodraw[i + 1] != 1:
    #                 self.painter.drawLine(points[i], points[i + 1])
    #             if nodraw[i] != 1 or nodraw[i + 4] != 1:
    #                 self.painter.drawLine(points[i], points[i + 4])
    #         if nodraw[0] != 1 or nodraw[3] != 1:
    #             self.painter.drawLine(points[0], points[3])
    #         if nodraw[3] != 1 or nodraw[7] != 1:
    #             self.painter.drawLine(points[3], points[7])
    #         for i in range(4, 7):
    #             if nodraw[i] != 1 or nodraw[i + 1] != 1:
    #                 self.painter.drawLine(points[i], points[i + 1])
    #         if nodraw[4] != 1 or nodraw[7] != 1:
    #             self.painter.drawLine(points[4], points[7])

    def avp(self, p1, p2, p3, p4):
        d1 = math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)
        d2 = math.sqrt(p2[0] ** 2 + p2[1] ** 2 + p2[2] ** 2)
        d3 = math.sqrt(p3[0] ** 2 + p3[1] ** 2 + p3[2] ** 2)
        d4 = math.sqrt(p4[0] ** 2 + p4[1] ** 2 + p4[2] ** 2)
        return (d1 + d2 + d3 + d4) / 4

    def sortV(self, avg, pols):
        new = []
        for i in range(len(avg)):
            counter = 0;
            max = 0
            for j in range(len(avg)):
                if avg[j]>max:
                    max = avg[j]
                    counter=j
            del avg[counter]
            new.append(pols[counter])
            del pols[counter]
        return new



    def paint(self):
        figures = self.rotate.data
        polygons = []
        avg = []
        for figure in figures:
            points = []
            for point in figure:
                x, y = self.recalculate(point)
                points.append(QPointF(x, y))

            polygons.append(QPolygonF([points[0], points[1], points[2], points[3]]))  # przód
            avg.append(self.avp(figure[0], figure[1], figure[2], figure[3]))
            polygons.append(QPolygonF([points[4], points[5], points[6], points[7]]))  # tył
            avg.append(self.avp(figure[4], figure[5], figure[6], figure[7]))
            polygons.append(QPolygonF([points[0], points[1], points[5], points[4]]))  # dół
            avg.append(self.avp(figure[0], figure[1], figure[5], figure[4]))
            polygons.append(QPolygonF([points[2], points[3], points[7], points[6]]))  # góra
            avg.append(self.avp(figure[2], figure[3], figure[7], figure[6]))
            polygons.append(QPolygonF([points[0], points[3], points[7], points[4]]))  # lewo
            avg.append(self.avp(figure[0], figure[3], figure[7], figure[4]))
            polygons.append(QPolygonF([points[1], points[2], points[6], points[5]]))  # prawo
            avg.append(self.avp(figure[1], figure[2], figure[6], figure[5]))
        polygons = self.sortV(avg, polygons)
        for pol in polygons:
            self.painter.drawPolygon(pol)
            self.colorCheck += 1
            if (self.colorCheck == 6):
                self.colorCheck = 0
            self.painter.setBrush(QBrush(self.colors[self.colorCheck] , Qt.SolidPattern))
