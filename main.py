from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys
import time
import signal
import lorenz
import util


signal.signal(signal.SIGINT, signal.SIG_DFL)


class AppGUI(QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.steps_min = 10
        self.steps_max = 10000
        self.steps = 1000

        self.dt = 0.001
        self.dt_min = 0.0001
        self.dt_max = 0.1
        # self.dt = 1

        self.color = 1

        self.p = np.zeros((self.steps, 3), dtype=np.float64)
        self.p[0] = np.array([1, 0, 0]) # initial conditions

        self.s = 10
        self.r = 28
        self.b = 8/3

        self.s_min = 0.5
        self.s_max = 60
        self.r_min = 0.5
        self.r_max = 60
        self.b_min = 0.1
        self.b_max = 10
        # self.b_max = 1



        # self.lastPosition = np.array([0,0,-10])


        self.init_ui()
        self.qt_connections()

        lorenz.lorenz(self.p, self.s, self.r, self.b, self.steps, self.dt)
        lorenz.lorenz(self.p, self.s_slider.value(), self.r_slider.value(), self.b_slider.value(), self.steps, self.dt)


        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.start(0)


    def init_ui(self):
        # pg.setConfigOption('background', 'w')
        # pg.setConfigOption('imageAxisOrder', 'row-major')

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.setWindowTitle('Lorenz Attractor')
        # self.win = pg.GraphicsWindow(title='A 2d plot window')

        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 100
        # self.w.opts['viewport'] = (0, 0, 400, 400)
        # self.w.setWindowTitle('pyqtgraph example: GLLine`em')
        # self.w.setGeometry(0, 110, 700, 700)
        # self.w.setMaximumHeight(100)
        grid_shift = 100

        grid_spacing = 25

        gx = gl.GLGridItem()
        gx.setSize(grid_shift, grid_shift, grid_shift)
        gx.rotate(90, 0, 1, 0)
        gx.translate(-grid_shift/2, 0, grid_shift/2)
        gx.setSpacing(grid_spacing, grid_spacing, grid_spacing)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.setSize(grid_shift, grid_shift, grid_shift)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -grid_shift/2, grid_shift/2)
        gy.setSpacing(grid_spacing, grid_spacing, grid_spacing)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.setSize(grid_shift, grid_shift, grid_shift)
        gz.setSpacing(grid_spacing, grid_spacing, grid_spacing)

        # gz.translate(0, 0, -grid_shift/2)
        self.w.addItem(gz)



        # self.color = (1, 0, 0, 1)

        self.main_scatter_plot = gl.GLScatterPlotItem()
        self.w.addItem(self.main_scatter_plot)




        projections_height = 80
        projections_width = 300

        self.xplot = pg.PlotWidget()
        self.xplot.showGrid(x=True, y=True, alpha=0.1)
        # self.xplot.enableAutoRange()
        self.xcurve = self.xplot.plot(pen='b')
        self.xplot.setFixedSize(projections_width, projections_height)

        self.yplot = pg.PlotWidget()
        self.yplot.showGrid(x=True, y=True, alpha=0.1)
        # self.yplot.enableAutoRange()
        self.ycurve = self.yplot.plot(pen='b')
        self.yplot.setFixedSize(projections_width, projections_height)

        self.zplot = pg.PlotWidget()
        self.zplot.showGrid(x=True, y=True, alpha=0.1)
        # self.zplot.enableAutoRange()
        self.zcurve = self.zplot.plot(pen='b')
        self.zplot.setFixedSize(projections_width, projections_height)


        self.projections_1d_layout = QtGui.QVBoxLayout()


        # layoutgb = QtGui.QGridLayout()
        self.layout = QtGui.QHBoxLayout()
        self.right_layout = QtGui.QVBoxLayout()
        self.left_layout = QtGui.QVBoxLayout()

        self.steps_label = QtGui.QLabel()
        self.dt_label = QtGui.QLabel()
        self.s_label = QtGui.QLabel()
        self.r_label = QtGui.QLabel()
        self.b_label = QtGui.QLabel()


        self.sliders_positions = 2000

        self.s_label.setStyleSheet('background-color: rgba(255, 0, 0, 0.2)')


        self.steps_slider = QtGui.QSlider(orientation=QtCore.Qt.Horizontal)
        self.steps_slider.setValue(self.steps)
        self.steps_slider.setRange(self.steps_min, self.steps_max)
        self.steps_slider.setTickInterval(1000)

        self.dt_slider = QtGui.QSlider(orientation=QtCore.Qt.Horizontal)
        self.dt_slider.setValue(self.dt)
        self.dt_slider.setRange(0, self.sliders_positions)



        self.s_slider = QtGui.QSlider(orientation=QtCore.Qt.Horizontal)
        self.s_slider.setRange(0, self.sliders_positions)
        self.s_slider.setValue(util.fit(self.s, self.s_min, self.s_max, 0, self.sliders_positions))
        # self.s_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        # self.s_slider.setTickInterval(0.1)


        self.r_slider = QtGui.QSlider(orientation=QtCore.Qt.Horizontal)
        self.r_slider.setRange(0, self.sliders_positions)
        self.r_slider.setValue(util.fit(self.r, self.r_min, self.r_max, 0, self.sliders_positions))
        # self.r_slider.setTickInterval(0.1)

        self.b_slider = QtGui.QSlider(orientation=QtCore.Qt.Horizontal)
        self.b_slider.setRange(0, self.sliders_positions)
        self.b_slider.setValue(util.fit(self.b, self.b_min, self.b_max, 0, self.sliders_positions))
        # self.b_slider.setTickInterval(0.01)


        self.color = np.array([
            (1*x, 0.2+0.5*x, 0.1+0.3*x, 1)
            for x in np.linspace(0, 1, self.steps)
        ])


        # pos = self.p, size = np.ones(self.p.shape[0]) * 0.3, color = self.color, pxMode = False


        sliders_width = 300
        self.steps_slider.setFixedWidth(sliders_width)
        self.dt_slider.setFixedWidth(sliders_width)
        self.s_slider.setFixedWidth(sliders_width)
        self.r_slider.setFixedWidth(sliders_width)
        self.b_slider.setFixedWidth(sliders_width)

        self.right_layout.addWidget(self.steps_slider)
        self.right_layout.addWidget(self.steps_label)
        self.right_layout.addWidget(self.dt_slider)
        self.right_layout.addWidget(self.dt_label)
        self.right_layout.addWidget(self.s_label)
        self.right_layout.addWidget(self.s_slider)
        self.right_layout.addWidget(self.r_label)
        self.right_layout.addWidget(self.r_slider)
        self.right_layout.addWidget(self.b_label)
        self.right_layout.addWidget(self.b_slider)

        self.right_layout.addWidget(self.xplot)
        self.right_layout.addWidget(self.yplot)
        self.right_layout.addWidget(self.zplot)

        self.params_changed()
        self.left_layout.addWidget(self.w)
        self.left_layout.addLayout(self.projections_1d_layout, stretch=2)

        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)

        self.setLayout(self.layout)

        self.setGeometry(0, 0, 1440, 900)
        # self.setGeometry(0, 0, 1200, 900)

    def qt_connections(self):
        self.steps_slider.valueChanged.connect(self.steps_changed)
        self.dt_slider.valueChanged.connect(self.params_changed)
        self.s_slider.valueChanged.connect(self.params_changed)
        self.r_slider.valueChanged.connect(self.params_changed)
        self.b_slider.valueChanged.connect(self.params_changed)

    def steps_changed(self):
        self.steps = self.steps_slider.value()
        self.p = np.zeros((self.steps, 3), dtype=np.float64)
        self.p[0] = np.array([1, 0, 0]) # initial conditions
        self.params_changed()

        self.color = np.array([
            (1*x, 0.2+0.5*x, 0.1+0.3*x, 1)
            for x in np.linspace(0, 1, self.steps)
        ])

        # print(self.p.shape)

    def params_changed(self):
        # print(self.p.min(), self.p.max())

        self.s = util.fit(self.s_slider.value(), 0, self.sliders_positions, self.s_min, self.s_max)
        self.r = util.fit(self.r_slider.value(), 0, self.sliders_positions, self.r_min, self.r_max)
        self.b = util.fit(self.b_slider.value(), 0, self.sliders_positions, self.b_min, self.b_max)
        self.dt = util.fit(self.dt_slider.value(), 0, self.sliders_positions, self.dt_min, self.dt_max)

        lorenz.lorenz(self.p, self.s, self.r, self.b, self.steps, self.dt)

        # self.main_scatter_plot.setData(pos=self.p, size=np.ones(self.p.shape[0])*0.3, color=self.color, pxMode=False)
        self.main_scatter_plot.setData(pos=self.p, size=0.3, color=self.color, pxMode=False)

        self.xcurve.setData(self.p[:, 0], connect='finite')
        self.ycurve.setData(self.p[:, 1], connect='finite')
        self.zcurve.setData(self.p[:, 2], connect='finite')

        print(self.steps, self.dt, f'min = {np.min(self.p)} max = {np.max(self.p)}')
        # self.xplot.setYRange(np.min(self.p[:, 0]), np.max(self.p[:, 0]))
        # self.yplot.setYRange(np.min(self.p[:, 1]), np.max(self.p[:, 0]))
        # self.zplot.setYRange(np.min(self.p[:, 2]), np.max(self.p[:, 1]))

        # print(self.steps)
        self.steps_label.setText(f'steps {self.steps}')
        self.dt_label.setText(f'dt {self.dt}')
        self.s_label.setText(f'σ {self.s}')
        self.r_label.setText(f'ρ {self.r}')
        self.b_label.setText(f'β {self.b}')



    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        sys.exit(0)

    def update(self):
        pass
        # self.dt = 0.015
        # self.dt = 0.012
        # self.dt = 0.12
        # print(np.random.random())

        # for i in range(self.stepCnt):
        #     # Derivatives of the X, Y, Z state
        #     x_dot, y_dot, z_dot = self.lorenz(
        #         self.p[i, 0], 
        #         self.p[i, 1],
        #         self.p[i, 2],
        #     )
        #     # x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i])

        #     self.p[i + 1, 0] = self.p[i, 0] + (x_dot * self.dt)
        #     self.p[i + 1, 1] = self.p[i, 1] + (y_dot * self.dt)
        #     self.p[i + 1, 2] = self.p[i, 2] + (z_dot * self.dt)

        # self.p = 1 * np.random.random(size=(self.stepCnt + 1, 3))

        # self.main_scatter_plot.setData(pos=self.p, size=np.ones(self.p.shape[0])*0.1, color=self.color, pxMode=False)


        # self.xcurve.setData(self.t_range, self.p[:, 0])
        # self.ycurve.setData(self.t_range, self.p[:, 1])
        # self.zcurve.setData(self.t_range, self.p[:, 2])

    # print('lol')
        # dx = (self.a * (self.y - self.x)) * self.dt
        # dy = (self.x * (self.b - self.z) - self.y) * self.dt
        # dz = (self.x * self.y - self.c * self.z) * self.dt
        # self.x = self.x + dx
        # self.y = self.y + dy
        # self.z = self.z + dz
        # position = np.array([self.x*.3,(self.y*.3),(self.z*.3)-10])
        # pts = np.vstack((self.lastPosition,position))
        # # newLine = gl.GLLinePlotItem(pos=pts,color=pg.mkColor(self.color),width=2)
        # newLine = gl.GLLinePlotItem(pos=pts,width=1)
        # self.color += 1
        # self.lastPosition = position
        # self.w.addItem(newLine)




# app = QtGui.QApplication.instance()

app = QtGui.QApplication(sys.argv)
# QtGui.QApplication.instance().exec()
gui = AppGUI()
gui.show()

app.exec()
# sys.exit(app.exec())
# sys.exit(app.exec())

# signal.signal(signal.SIGINT, signal.SIG_DFL)
# sys.exit(app.exec())
