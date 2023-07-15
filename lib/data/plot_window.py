import matplotlib

matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class RealTimeDataPlotter(QtWidgets.QWidget):

    def __init__(self, title, x, y, delta_t) -> None:
        super().__init__()
        self.__visible = False
        self.data = {}
        self.__options = ['r-', 'b-', 'g-']
        self.setWindowTitle(title)
        self.setMinimumSize(640, 480)
        self._graph_init()
        self.x = x
        self.y = y
        self.delta_t = delta_t
        self.timer = 0

    def _graph_init(self):
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.fig.tight_layout()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def add(self, varname, vardata):
        if varname in self.data:
            self.data[varname].append(vardata)
        else:
            self.data[varname] = [vardata]

    def plot(self, time):
        if time > self.timer + self.delta_t:
            if not self.__visible:
                self.__visible = True
                self.show()
            self.update()
            self.timer += self.delta_t

    def paintEvent(self, event):
        self.axes.clear()
        [x_axis, x_label] = self.x
        for i in range(0, len(self.y)):
            self.axes.plot(self.data[x_axis], self.data[self.y[i][0]], self.__options[i], label=self.y[i][1])
        self.axes.set_xlabel(x_label)
        self.axes.legend()
        self.canvas.draw()

    def exitCall(self) -> None:
        QtWidgets.QApplication.quit()

    def closeEvent(self, event) -> None:
        self.exitCall()
