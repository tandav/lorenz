import numpy as np

def lorenz(x, y, z, s=10, r=100, b=9)  :
# def lorenz(x, y, z, s=10, r=150, b=8/3)  :
# def lorenz(x, y, z, s=10.2, r=24, b=7)  :
    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z
    return x_dot, y_dot, z_dot

dt = 0.001
# dt = 1
    
stepCnt = 10000

# Need one more for the initial valuessin

# points
p = np.empty(shape=(stepCnt + 1, 3), dtype=np.float128)

# xs = np.empty((stepCnt + 1,), dtype=np.float128)
# ys = np.empty((stepCnt + 1,), dtype=np.float128)
# zs = np.empty((stepCnt + 1,), dtype=np.float128)

# Setting initial values
# xs[0], ys[0], zs[0] = (0., 1., 1.05)
# xs[0], ys[0], zs[0] = (0., 1., 1.05)

p[0] = np.array([1, 0, 0])

# Stepping through "time".

# todo: use numba everywhere
for i in range(stepCnt):
    # Derivatives of the X, Y, Z state
    x_dot, y_dot, z_dot = lorenz(
        p[i, 0], 
        p[i, 1],
        p[i, 2],
    )
    # x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i])

    p[i + 1, 0] = p[i, 0] + (x_dot * dt)
    p[i + 1, 1] = p[i, 1] + (y_dot * dt)
    p[i + 1, 2] = p[i, 2] + (z_dot * dt)


# embedding = np.random.random((100, 3))
# do all of the above, and then:
# embedding = umap.UMAP(n_components=3, metric='cosine', n_epochs=500).fit_transform(X)
## embedding = np.load('1e6_pts_3D.npz')['embedding']

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

scale = 400

app = QtGui.QApplication([])
w = gl.GLViewWidget()
# w.pan(-500,500,100)
# w.opts['viewport'] =  (0, 0, 800, 600)
w.opts['distance'] = scale
# w.showMaximized()

w.show()

# g = gl.GLGridItem()
# w.addItem(g)

gridsize = scale

gx = gl.GLGridItem()
gx.setSize(x=gridsize, y=gridsize, z=gridsize)
gx.rotate(90, 0, 1, 0)
gx.translate(-gridsize/2, 0, gridsize/2)
gx.setSpacing(gridsize//25, gridsize//25, gridsize//25)
w.addItem(gx)

gy = gl.GLGridItem()
gy.setSize(x=gridsize, y=gridsize, z=gridsize)
gy.rotate(90, 1, 0, 0)
gy.translate(0, -gridsize/2, gridsize/2)
gy.setSpacing(gridsize//25, gridsize//25, gridsize//25)
w.addItem(gy)

gz = gl.GLGridItem()
gz.setSize(x=gridsize, y=gridsize, z=gridsize)
# gz.translate(0, 0, -10)
# gz.translate(0, 0,0)
gz.setSpacing(gridsize//25, gridsize//25, gridsize//25)
w.addItem(gz)


color = np.array([(1*x, 0.2+0.5*x, 0.1+0.3*x, 1) for x in np.linspace(0, 1, p.shape[0]) ])

sp1 = gl.GLScatterPlotItem(pos=p, size=np.ones(p.shape[0])*0.2, color=color, pxMode=False)
sp1.translate(5,5,0)
w.addItem(sp1)


QtGui.QApplication.instance().exec_()
