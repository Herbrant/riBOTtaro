from matplotlib import pylab


class DataPlotter:

    def __init__(self):
        self.data = {}
        self.__options = ['r-', 'b-', 'g-']
        self.__figure_num = 1

    def add(self, varname, vardata):
        if varname in self.data:
            self.data[varname].append(vardata)
        else:
            self.data[varname] = [vardata]

    def plot(self, x, y):
        [x_axis, x_label] = x
        pylab.figure(self.__figure_num)
        for i in range(0, len(y)):
            pylab.plot(self.data[x_axis], self.data[y[i][0]], self.__options[i], label=y[i][1])
        pylab.xlabel(x_label)
        pylab.legend()
        self.__figure_num += 1

    def show(self):
        pylab.show()
