import math
import pathlib

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class CartWindow(QWidget):

    def __init__(self, _compound_sys):
        super(CartWindow, self).__init__()
        self.compound_system = _compound_sys
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1000, 400)
        self.setWindowTitle('Robot 1D Simulator')
        self.show()

        current_path = pathlib.Path(__file__).parent.resolve()
        image = str(current_path) + '/../icons/cart.png'

        self.robot_pic = QtGui.QPixmap(image)

        self._timer_painter = QtCore.QTimer(self)
        self._timer_painter.start(int(self.compound_system.delta_t * 1000))
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

        x_pos = 50 + (self.compound_system.get_pose() * 50)
        y_pos = 236

        qp.drawPixmap(int(x_pos), int(y_pos), self.robot_pic)

        qp.setPen(Qt.black)
        qp.drawLine(0, 281, 990, 281)
        qp.drawLine(0, 282, 990, 282)
        qp.drawLine(990, 281, 990 - 10, 281 - 10)
        qp.drawLine(990, 282, 990 - 10, 282 + 10)

        qp.drawText(850, 20, "t = %6.3f s" % self.compound_system.t)
        qp.drawText(850, 40, "P = %6.3f m" % (self.compound_system.get_pose()))
        qp.drawText(850, 60, "V = %6.3f m/s" % (self.compound_system.get_speed()))

        qp.end()


# -------------------------------------------------------------------------------

class ArmWindow(QWidget):

    def __init__(self, _compound_sys):
        super(ArmWindow, self).__init__()
        self.compound_system = _compound_sys
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1000, 400)
        self.setWindowTitle('Robot 1D Simulator')
        self.show()

        self._timer_painter = QtCore.QTimer(self)
        self._timer_painter.start(int(self.compound_system.delta_t * 1000))
        self._timer_painter.timeout.connect(self.go)

    def go(self):
        if not (self.compound_system.step()):
            self._timer_painter.stop()
        self.update()  # repaint window

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)

        th = self.compound_system.get_pose()
        omega = self.compound_system.get_speed()

        x = int(200 * self.compound_system.arm.r * math.sin(th))
        y = int(200 * self.compound_system.arm.r * math.cos(th))

        self.__draw_arm_element(qp, 500, 20, x + 500, y + 20)

        qp.drawText(800, 20, "t = %6.3f s" % (self.compound_system.t))
        qp.drawText(800, 40, "Theta = %6.3f deg" % (math.degrees(th)))
        qp.drawText(800, 60, "Omega = %6.3f rad/s" % (omega))

        qp.end()

    def __draw_arm_element(self, qp, x1, y1, x2, y2, ellipse=True):
        qp.setPen(QtGui.QPen(Qt.black, 8))
        qp.drawLine(x1, y1, x2, y2)

        if ellipse:
            qp.setPen(QtGui.QPen(Qt.red, 3))

            qp.drawEllipse(QtCore.QPoint(x1, y1), 10, 10)
            qp.drawEllipse(QtCore.QPoint(x1, y1), 4, 4)

            qp.setPen(QtGui.QPen(Qt.black, 3))

            qp.drawEllipse(QtCore.QPoint(x2, y2), 10, 10)
            qp.drawEllipse(QtCore.QPoint(x2, y2), 4, 4)
