from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class ManipulatorWindow(QWidget):
    x_center = 50
    y_center = 400

    def __init__(self, _compound_sys):
        super(ManipulatorWindow, self).__init__()
        self.compound_system = _compound_sys
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1000, 600)
        self.setWindowTitle('Robotic Arm Simulator')
        self.show()

        self.delta_t = self.compound_system.delta_t

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

        qp.setPen(Qt.black)
        qp.drawLine(50, 500, 900, 500)
        qp.drawLine(50, 500, 50, 50)
        qp.drawLine(50, 50, 900, 50)
        qp.drawLine(900, 50, 900, 500)

        qp.setPen(Qt.black)

        th = self.compound_system.get_pose_degrees()
        p = self.compound_system.get_joint_positions()
        (x1, y1) = p[0]
        (x2, y2) = p[1]
        (x3, y3) = p[2]
        qp.drawText(910, 20, "X  = %6.3f m" % (x2))
        qp.drawText(910, 40, "Y  = %6.3f m" % (y2))
        qp.drawText(910, 60, "Th1= %6.3f deg" % (th[0]))
        qp.drawText(910, 80, "Th2= %6.3f deg" % (th[1]))
        qp.drawText(910, 100, "Th3= %6.3f deg" % (th[2]))
        qp.drawText(910, 120, "T  = %6.3f s" % (self.compound_system.t))

        (x1_pos, y1_pos) = self.__xy_to_pixel(x1, y1)
        (x2_pos, y2_pos) = self.__xy_to_pixel(x2, y2)
        (x3_pos, y3_pos) = self.__xy_to_pixel(x3, y3)

        self.__draw_arm_element(qp, ManipulatorWindow.x_center, ManipulatorWindow.y_center, x1_pos, y1_pos)
        self.__draw_arm_element(qp, x1_pos, y1_pos, x2_pos, y2_pos)
        self.__draw_arm_element(qp, x2_pos, y2_pos, x3_pos, y3_pos, False)

        qp.end()

    def __draw_arm_element(self, qp, x1, y1, x2, y2, ellipse=True):
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        qp.setPen(QtGui.QPen(Qt.black, 8))
        qp.drawLine(x1, y1, x2, y2)

        if ellipse:
            qp.setPen(QtGui.QPen(Qt.black, 3))

            qp.drawEllipse(QtCore.QPoint(x1, y1), 10, 10)
            qp.drawEllipse(QtCore.QPoint(x1, y1), 4, 4)

            qp.drawEllipse(QtCore.QPoint(x2, y2), 10, 10)
            qp.drawEllipse(QtCore.QPoint(x2, y2), 4, 4)

    def __xy_to_pixel(self, x, y):
        return ManipulatorWindow.x_center + x * 1000, ManipulatorWindow.y_center - y * 1000
