class Proportional:

    def __init__(self, kp):
        self.kp = kp

    def evaluate(self, target, current):
        error = target - current
        return self.kp * error

    def evaluate_error(self, error):
        return self.kp * error


class Integral:

    def __init__(self, ki):
        self.ki = ki
        self.output = 0

    def evaluate(self, delta_t, target, current):
        error = target - current
        self.output = self.output + self.ki * error * delta_t
        return self.output

    def evaluate_error(self, delta_t, error):
        self.output = self.output + self.ki * error * delta_t
        return self.output


class ProportionalIntegral:

    def __init__(self, kp, ki):
        self.p = Proportional(kp)
        self.i = Integral(ki)

    def evaluate(self, delta_t, target, current):
        return self.p.evaluate(target, current) + self.i.evaluate(delta_t, target, current)


class PID:

    def __init__(self, kp, ki, kd):
        self.p = Proportional(kp)
        self.i = Integral(ki)
        self.kd = kd
        self.prev_error = 0

    def evaluate(self, delta_t, target, current):
        error = target - current
        derivative = (error - self.prev_error) / delta_t
        self.prev_error = error
        return self.p.evaluate(target, current) + self.i.evaluate(delta_t, target, current) + \
            derivative * self.kd


class PIDSat:

    def __init__(self, kp, ki, kd, saturation, antiwindup=False):
        self.p = Proportional(kp)
        self.i = Integral(ki)
        self.kd = kd
        self.prev_error = 0
        self.saturation = saturation
        self.antiwindup = antiwindup
        self.in_saturation = False

    def evaluate(self, delta_t, target, current):
        error = target - current
        derivative = (error - self.prev_error) / delta_t
        self.prev_error = error
        if not (self.antiwindup):
            self.i.evaluate(delta_t, target, current)
        elif not (self.in_saturation):
            self.i.evaluate(delta_t, target, current)
        output = self.p.evaluate(target, current) + self.i.output + \
                 derivative * self.kd
        if output > self.saturation:
            output = self.saturation
            self.in_saturation = True
        elif output < -self.saturation:
            output = - self.saturation
            self.in_saturation = True
        else:
            self.in_saturation = False
        return output

    def evaluate_error(self, delta_t, error):
        derivative = (error - self.prev_error) / delta_t
        self.prev_error = error
        if not (self.antiwindup):
            self.i.evaluate_error(delta_t, error)
        elif not (self.in_saturation):
            self.i.evaluate_error(delta_t, error)
        output = self.p.evaluate_error(error) + self.i.output + \
                 derivative * self.kd
        if output > self.saturation:
            output = self.saturation
            self.in_saturation = True
        elif output < -self.saturation:
            output = - self.saturation
            self.in_saturation = True
        else:
            self.in_saturation = False
        return output
