import math

# Standard Acceleration of Gravity
G: float = 9.81


class Arm:

    def __init__(self, _mass: float, _friction: float, _length: float):
        """
        Defines an arm robot with the given mass, friction and bar length
        :param _mass: The mass attached at the end of the bar, expressed in Kg
        :param _friction: The force of friction present in the system
        :param _length: The bar's length
        """
        self.M: float = _mass
        self.b: float = _friction
        self.r: float = _length
        self.omega: float = 0
        self.theta: float = 0

    def evaluate(self, delta_t: float, _torque: float) -> None:
        """
        Evaluates the angular speed and angular position at the given time with the applied torque
        :param delta_t: The delta time
        :param _torque: The Applied torque
        """
        new_omega: float = self.omega - ((self.b * self.r) / self.M) * delta_t * self.omega \
                           - G * delta_t * self.theta + delta_t / (self.M * self.r) * _torque
        new_theta: float = self.theta + self.omega * delta_t
        self.omega = new_omega
        self.theta = new_theta

    def evaluate_no_approx(self, delta_t: float, _torque: float) -> None:
        """
        Evaluates without approximation the angular speed and angular position at the given time with the applied torque
        :param delta_t: The delta time
        :param _torque: The applied torque
        """
        new_omega: float = self.omega - ((self.b * self.r) / self.M) * delta_t * self.omega \
                           - G * delta_t * math.sin(self.theta) + delta_t / (self.M * self.r) * _torque
        new_theta: float = self.theta + self.omega * delta_t
        self.omega = new_omega
        self.theta = new_theta
