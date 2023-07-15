import math
import pathlib

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget


class MultirotorWindow(QWidget):

    def __init__(self, _compound_sys):
        super(MultirotorWindow, self).__init__()
        self.compound_system = _compound_sys
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1000, 600)
        self.setWindowTitle('QuadRotor 2D Simulator')
        self.show()

        current_path = pathlib.Path(__file__).parent.resolve()
        image = str(current_path) + '/../icons/drone.png'

        self.drone = QtGui.QPixmap(image)

        self.delta_t = 1e-3  # 1ms of time-tick

        self._timer_painter = QtCore.QTimer(self)
        self._timer_painter.start(int(self.delta_t * 1000))
        self._timer_painter.timeout.connect(self.go)

    def go(self):
        if not (self.compound_system.step()):
            self._timer_painter.stop()
        self.update()  # repaint window

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.setBrush(QtGui.QColor(255, 255, 255))
        qp.drawRect(event.rect())

        (x, z, theta) = self.compound_system.get_pose()
        (vx, vz, omega) = self.compound_system.get_speed()

        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.drawText(850, 20, "X = %6.3f m" % (x))
        qp.drawText(850, 40, "Vx = %6.3f m/s" % (vx))
        qp.drawText(850, 60, "Z = %6.3f m" % (z))
        qp.drawText(850, 80, "Vz = %6.3f m/s" % (vz))
        qp.drawText(850, 100, "Th = %6.3f deg" % (math.degrees(theta)))
        qp.drawText(850, 120, "Omega = %6.3f deg" % (math.degrees(omega)))

        s = self.drone.size()

        x_pos = int(50 + x * 1000 - s.width() / 2)
        y_pos = int(500 - z * 1000 - s.height() / 2)

        t = QtGui.QTransform()
        t.translate(x_pos + s.height() / 2, y_pos + s.width() / 2)
        t.rotate(-math.degrees(theta))
        t.translate(-(x_pos + s.height() / 2), - (y_pos + s.width() / 2))

        qp.setTransform(t)
        qp.drawPixmap(x_pos, y_pos, self.drone)

        qp.end()
