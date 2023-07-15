class Impulse:

    def __init__(self, amount):
        self.u = amount

    def evaluate(self, delta_t):
        output = self.u
        self.u = 0
        return output


# ------------------------------------------------------

class Step:

    def __init__(self, amount):
        self.u = amount

    def evaluate(self, delta_t):
        return self.u


# ------------------------------------------------------

class Ramp:

    def __init__(self, rate):
        self.rate = rate
        self.u = 0

    def evaluate(self, delta_t):
        output = self.u
        self.u += self.rate * delta_t
        return output


# ------------------------------------------------------

class RampSat(Ramp):

    def __init__(self, rate, outmax):
        super().__init__(rate)
        self.outmax = outmax

    def evaluate(self, delta_t):
        output = super().evaluate(delta_t)
        if output > self.outmax:
            output = self.outmax
        return output
