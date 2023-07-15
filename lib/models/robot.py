class RoboticSystem:

    def __init__(self, delta_t):
        self.delta_t = delta_t
        self.t = 0

    def step(self):
        v = self.run()
        self.t = self.t + self.delta_t
        return v

    def run(self):
        raise 'Not implemented'

    def get_pose(self):
        raise 'Not implemented'

    def get_speed(self):
        raise 'Not implemented'



