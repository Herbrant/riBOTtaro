import math


class Multirotor2D:

    def __init__(self, _m, _L):
        self.L = _L
        self.M = _m
        self.I = (_m * (_L / 2.0) ** 2) / 12.0
        self.omega = 0
        self.theta = 0
        self.b = 0.8
        self.vx = 0
        self.x = 0
        self.vz = 0
        self.z = 0

    def evaluate(self, delta_t, f1, f2):
        # traslation dynamics over Z
        self.z = self.z + self.vz * delta_t
        self.vz = (1 - delta_t * self.b / self.M) * self.vz + \
                  delta_t * (f1 + f2) * math.cos(self.theta) / self.M - 9.81 * delta_t
        if self.z < 0:
            self.z = 0
            self.vz = 0
        # traslation dynamics over X
        self.x = self.x + self.vx * delta_t
        self.vx = (1 - delta_t * self.b / self.M) * self.vx + delta_t * (f1 + f2) * math.sin(-self.theta) / self.M
        # rotation dynamics
        self.theta = self.theta + self.omega * delta_t
        self.omega = (1 - self.b * self.L * delta_t / self.I) * self.omega + delta_t * (f2 - f1) * self.L / self.I
