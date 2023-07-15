class FileReader:

    def __init__(self, _filename):
        self.filename = _filename

    def load(self):
        f = open(self.filename, 'r')
        lines = f.readlines()
        f.close()
        first_line = lines[0]
        self.columns = [x.strip() for x in first_line[1:].split(',')]
        self.data = []
        for l in lines[1:]:
            data = [float(x) for x in l.split(',')]
            self.data.append(data)
        self.current = None

    def get_vars(self, t, varlist):
        if self.current is None:
            self.current = self.__get_index_from_time(t)
        else:
            self.current = self.__verify_index_from_time(t)
        if self.current is None:
            return []
        values = []
        for v in varlist:
            i = self.columns.index(v)
            if i >= 0:
                values.append(self.data[self.current][i])
        return values

    def __get_index_from_time(self, t):
        i = 0
        while i < len(self.data) - 1:
            if (t >= self.data[i][0]) and (t < self.data[i + 1][0]):
                return i
            i = i + 1
        if t >= self.data[i][0]:
            return i
        else:
            return None

    def __verify_index_from_time(self, t):
        if self.current == len(self.data) - 1:
            if t >= self.data[self.current][0]:
                return self.current
            else:
                return self.__get_index_from_time(t)
        else:
            if (t >= self.data[self.current][0]) and (t < self.data[self.current + 1][0]):
                return self.current
            else:
                return self.__get_index_from_time(t)
