from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
import time

class Visualizer(object):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        self.w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
        self.w.setGeometry(0, 110, 700, 700)
        self.w.show()
        self.dt = 0.015



        # gx = gl.GLGridItem()
        # gx.rotate(90, 0, 1, 0)
        # gx.translate(-10, 0, 0)
        # self.w.addItem(gx)
        # gy = gl.GLGridItem()
        # gy.rotate(90, 1, 0, 0)
        # gy.translate(0, -10, 0)
        # self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -10)
        self.w.addItem(gz)
        self.color = 1
        self.x = 0.01
        self.y = 0
        self.z = 0

        self.a = 10
        self.b = 28
        self.c = 8/3
        self.lastPosition = np.array([0,0,-10])


        


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()



    def update(self):
        dx = (self.a * (self.y - self.x)) * self.dt
        dy = (self.x * (self.b - self.z) - self.y) * self.dt
        dz = (self.x * self.y - self.c * self.z) * self.dt
        self.x = self.x + dx
        self.y = self.y + dy
        self.z = self.z + dz
        position = np.array([self.x*.3,(self.y*.3),(self.z*.3)-10])
        pts = np.vstack((self.lastPosition,position))
        # newLine = gl.GLLinePlotItem(pos=pts,color=pg.mkColor(self.color),width=2)
        newLine = gl.GLLinePlotItem(pos=pts,width=1)
        self.color += 1
        self.lastPosition = position
        self.w.addItem(newLine)



        



    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0)
        self.start()


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    v = Visualizer()
    v.animation()
