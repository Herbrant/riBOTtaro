import math
from lib.controllers.standard import PIDSat
from lib.models.virtual_robot import VirtualRobot
from lib.data.geometry import normalize_angle


class Polar2DController:

    def __init__(self, KP_linear, v_max, KP_heading, w_max):
        self.linear = PIDSat(KP_linear, 0, 0, v_max)
        self.angular = PIDSat(KP_heading, 0, 0, w_max)

    def evaluate(self, delta_t, xt, yt, current_pose):
        (x, y, theta) = current_pose

        dx = xt - x
        dy = yt - y

        target_heading = math.atan2(dy, dx)

        distance = math.sqrt(dx * dx + dy * dy)
        heading_error = normalize_angle(target_heading - theta)

        if (heading_error > math.pi / 2) or (heading_error < -math.pi / 2):
            distance = -distance
            heading_error = normalize_angle(heading_error + math.pi)

        v_target = self.linear.evaluate_error(delta_t, distance)
        w_target = self.angular.evaluate_error(delta_t, heading_error)

        return v_target, w_target


class StraightLine2DMotion:

    def __init__(self, _vmax, _acc, _dec):
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec

    def start_motion(self, start, end):
        (self.xs, self.ys) = start
        (self.xe, self.ye) = end

        dx = self.xe - self.xs
        dy = self.ye - self.ys

        self.heading = math.atan2(dy, dx)
        self.distance = math.sqrt(dx * dx + dy * dy)

        self.virtual_robot = VirtualRobot(self.distance, self.vmax, self.accel, self.decel)

    def evaluate(self, delta_t):
        self.virtual_robot.evaluate(delta_t)

        xt = self.xs + self.virtual_robot.p * math.cos(self.heading)
        yt = self.ys + self.virtual_robot.p * math.sin(self.heading)

        return xt, yt


class Path2D:

    def __init__(self, _vmax, _acc, _dec, _threshold):
        self.threshold = _threshold
        self.path = []
        self.trajectory = StraightLine2DMotion(_vmax, _acc, _dec)

    def set_path(self, path):
        self.path = path

    def start(self, start_pos):
        self.current_target = self.path.pop(0)
        self.trajectory.start_motion(start_pos, self.current_target)

    def evaluate(self, delta_t, pose):
        (x, y) = self.trajectory.evaluate(delta_t)
        self.x_current = x
        self.y_current = y
        target_distance = math.hypot(pose[0] - self.current_target[0],
                                     pose[1] - self.current_target[1])
        if target_distance < self.threshold:
            if len(self.path) == 0:
                return None
            else:
                self.start((x, y))

        return x, y
