import math

from lib.data.geometry import normalize_angle


class A_VirtualRobot:
    ACCEL = 0
    CRUISE = 1
    DECEL = 2
    TARGET = 3

    def __init__(self, _p_target, _vmax, _acc, _dec):
        self.p_target = _p_target
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec
        self.v = 0  # current speed
        self.p = 0  # current position
        self.phase = A_VirtualRobot.ACCEL
        self.decel_distance = 0.5 * _vmax * _vmax / _dec

    def evaluate(self, delta_t):
        if self.phase == A_VirtualRobot.ACCEL:
            self.p = self.p + self.v * delta_t \
                     + self.accel * delta_t * delta_t / 2
            self.v = self.v + self.accel * delta_t
            if self.v >= self.vmax:
                self.v = self.vmax
                self.phase = A_VirtualRobot.CRUISE
            elif self.p_target - self.p <= self.decel_distance:
                self.phase = A_VirtualRobot.DECEL

        elif self.phase == A_VirtualRobot.CRUISE:
            self.p = self.p + self.vmax * delta_t
            if self.p_target - self.p <= self.decel_distance:
                self.phase = A_VirtualRobot.DECEL

        elif self.phase == A_VirtualRobot.DECEL:
            self.p = self.p + self.v * delta_t \
                     - self.decel * delta_t * delta_t / 2
            self.v = self.v - self.decel * delta_t
            if self.p >= self.p_target:
                self.v = 0
                self.p = self.p_target
                self.phase = A_VirtualRobot.TARGET


# ------------------------------------------------------------

class VirtualRobot:
    ACCEL = 0
    CRUISE = 1
    DECEL = 2
    TARGET = 3

    def __init__(self, _p_target, _vmax, _acc, _dec):
        self.p_target = _p_target
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec
        self.v = 0  # current speed
        self.p = 0  # current position
        self.phase = VirtualRobot.ACCEL
        self.decel_distance = 0.5 * _vmax * _vmax / _dec

    def evaluate(self, delta_t):
        if self.phase == VirtualRobot.ACCEL:
            self.p = self.p + self.v * delta_t \
                     + self.accel * delta_t * delta_t / 2
            self.v = self.v + self.accel * delta_t
            distance = self.p_target - self.p
            if distance < 0:
                distance = 0
            if self.v >= self.vmax:
                self.v = self.vmax
                self.phase = VirtualRobot.CRUISE
            elif distance <= self.decel_distance:
                v_exp = math.sqrt(2 * self.decel * distance)
                if v_exp < self.v:
                    self.phase = VirtualRobot.DECEL

        elif self.phase == VirtualRobot.CRUISE:
            self.p = self.p + self.vmax * delta_t
            distance = self.p_target - self.p
            if distance <= self.decel_distance:
                self.phase = VirtualRobot.DECEL

        elif self.phase == VirtualRobot.DECEL:
            self.p = self.p + self.v * delta_t \
                     - self.decel * delta_t * delta_t / 2
            self.v = self.v - self.decel * delta_t
            if self.p >= self.p_target:
                self.v = 0
                self.p = self.p_target
                self.phase = VirtualRobot.TARGET


# ------------------------------------------------------------

class VirtualRobot2D:
    ACCEL = 0
    CRUISE = 1
    DECEL = 2
    TARGET = 3

    def __init__(self, _vmax, _acc, _dec):
        self.linear_trajectory = VirtualRobot(0, _vmax, _acc, _dec)

    def set_target(self, starting, target):
        self.starting = starting
        dx = target[0] - starting[0]
        dy = target[1] - starting[1]

        self.linear_target = math.hypot(dx, dy)
        self.target_heading = math.atan2(dy, dx)

        self.linear_trajectory.p_target = self.linear_target

    def evaluate(self, delta_t):
        self.linear_trajectory.evaluate(delta_t)
        x = self.starting[0] + self.linear_trajectory.p * math.cos(self.target_heading)
        y = self.starting[1] + self.linear_trajectory.p * math.sin(self.target_heading)
        return x, y


# ------------------------------------------------------------

class _SpeedProfileGenerator:
    ACCEL = 0
    CRUISE = 1
    DECEL = 2
    TARGET = 3

    def __init__(self, _p_target, _vmax, _acc, _dec):
        self.p_target = _p_target
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec
        self.v = 0  # current speed
        self.phase = SpeedProfileGenerator.ACCEL
        self.decel_distance = 0.5 * _vmax * _vmax / _dec

    def evaluate(self, delta_t, current_pos):
        # Indeed this is not correct!!
        # We should consider that, if the target is overcome, we must go back!!
        if current_pos >= self.p_target:
            self.v = 0
            self.phase = SpeedProfileGenerator.TARGET
            return

        distance = self.p_target - current_pos
        if self.phase == SpeedProfileGenerator.ACCEL:
            self.v = self.v + self.accel * delta_t
            if self.v >= self.vmax:
                self.v = self.vmax
                self.phase = SpeedProfileGenerator.CRUISE
            elif distance <= self.decel_distance:
                v_exp = math.sqrt(2 * self.decel * distance)
                if v_exp < self.v:
                    self.phase = SpeedProfileGenerator.DECEL

        elif self.phase == SpeedProfileGenerator.CRUISE:
            if distance <= self.decel_distance:
                self.phase = SpeedProfileGenerator.DECEL

        elif self.phase == SpeedProfileGenerator.DECEL:
            self.v = math.sqrt(2 * self.decel * distance)


# ------------------------------------------------------------

class SpeedProfileGenerator:
    ACCEL = 0
    CRUISE = 1
    DECEL = 2
    TARGET = 3

    def __init__(self, _p_target, _vmax, _acc, _dec):
        self.p_target = _p_target
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec
        self.v = 0  # current speed
        self.vp = 0  # current POSTIVE speed
        self.phase = SpeedProfileGenerator.ACCEL
        self.decel_distance = 0.5 * _vmax * _vmax / _dec

    def set_target(self, p):
        self.p_target = p

    def evaluate(self, delta_t, current_pos):
        distance = self.p_target - current_pos
        if distance == 0:
            self.v = 0
            self.vp = 0
            self.phase = SpeedProfileGenerator.TARGET
            return 0
        elif distance < 0:
            distance = -distance
            sign = -1
        else:
            sign = 1

        if self.phase == SpeedProfileGenerator.ACCEL:
            self.vp = self.vp + self.accel * delta_t
            if self.vp >= self.vmax:
                self.vp = self.vmax
                self.phase = SpeedProfileGenerator.CRUISE
            elif distance <= self.decel_distance:
                v_exp = math.sqrt(2 * self.decel * distance)
                if v_exp < self.vp:
                    self.phase = SpeedProfileGenerator.DECEL

        elif self.phase == SpeedProfileGenerator.CRUISE:
            if distance <= self.decel_distance:
                self.phase = SpeedProfileGenerator.DECEL

        elif self.phase == SpeedProfileGenerator.DECEL:
            self.vp = math.sqrt(2 * self.decel * distance)

        self.v = sign * self.vp
        return self.v


# ------------------------------------------------------------

class SpeedProfileGenerator2D:
    ACCEL = 0
    CRUISE = 1
    DECEL = 2
    TARGET = 3

    def __init__(self, _p_target, _vmax, _acc, _dec):
        self.p_target = _p_target
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec
        self.v = 0  # current speed
        self.vp = 0  # current POSTIVE speed
        self.phase = SpeedProfileGenerator.ACCEL
        self.decel_distance = 0.5 * _vmax * _vmax / _dec

    def set_target(self, p):
        self.p_target = p
        self.v = 0  # current speed
        self.vp = 0  # current POSTIVE speed
        self.phase = SpeedProfileGenerator.ACCEL

    def evaluate(self, delta_t, current_pos):
        dx = self.p_target[0] - current_pos[0]
        dy = self.p_target[1] - current_pos[1]

        distance = math.hypot(dy, dx)
        self.target_heading = math.atan2(dy, dx)

        heading_error = normalize_angle(self.target_heading - current_pos[2])

        if (heading_error > math.pi / 2) or (heading_error < -math.pi / 2):
            self.target_heading = normalize_angle(self.target_heading + math.pi)
            distance = -distance

        if distance == 0:
            self.v = 0
            self.vp = 0
            self.phase = SpeedProfileGenerator.TARGET
            return 0
        elif distance < 0:
            distance = -distance
            sign = -1
        else:
            sign = 1

        if self.phase == SpeedProfileGenerator.ACCEL:
            self.vp = self.vp + self.accel * delta_t
            if self.vp >= self.vmax:
                self.vp = self.vmax
                self.phase = SpeedProfileGenerator.CRUISE
            elif distance <= self.decel_distance:
                v_exp = math.sqrt(2 * self.decel * distance)
                if v_exp < self.vp:
                    self.phase = SpeedProfileGenerator.DECEL

        elif self.phase == SpeedProfileGenerator.CRUISE:
            if distance <= self.decel_distance:
                self.phase = SpeedProfileGenerator.DECEL

        elif self.phase == SpeedProfileGenerator.DECEL:
            self.vp = math.sqrt(2 * self.decel * distance)

        self.v = sign * self.vp
        return self.v


# ------------------------------------------------------------

class PlanarArmTrajectory:

    def __init__(self, vmax, accel, decel):
        self.vmax = vmax
        self.accel = accel
        self.decel = decel
        self.target_pos = 0
        self.target_heading = 0
        self.virtual_pos = 0
        self.virtual_speed = 0
        self.decel_distance = self.vmax * self.vmax / (2 * self.decel)
        self.accel_distance = self.vmax * self.vmax / (2 * self.accel)
        self.arm = None
        self.target_got = False

    def set_target(self, current, target):
        self.virtual_pos = 0
        self.virtual_speed = 0

        (current_x, current_y, current_alpha) = current
        (target_x, target_y, target_alpha) = target

        dx = target_x - current_x
        dy = target_y - current_y
        dz = target_alpha - current_alpha

        self.target_alpha = target_alpha

        # sferic coordinates
        self.target_pos = math.sqrt(dx**2 + dy**2 + dz**2)
        self.target_theta = math.atan2(math.hypot(dx,dy), dz)
        self.target_phi = math.atan2(dy, dx)

        self.start_x = current_x
        self.start_y = current_y
        self.start_alpha = current_alpha

        self.target_x = target_x
        self.target_y = target_y
        self.target_alpha = target_alpha

        self.target_got = False
        self.target_count = 0

        #print('------------------------------------------------')
        #print(self.start_x, self.start_y, self.start_alpha)
        #print(target_x, target_y, target_alpha)
        #print(self.target_pos, math.degrees(self.target_theta), math.degrees(self.target_phi))
        #import time
        #time.sleep(1)


    def evaluate(self, delta_t):
        distance = self.target_pos - self.virtual_pos

        if distance < self.decel_distance:
            arg = self.vmax * self.vmax - 2 * self.decel * (self.decel_distance - distance)
            if arg < 0:
                current_accel = 0
                self.virtual_speed = 0
            else:
                vel_attesa = math.sqrt(arg)
                if vel_attesa > self.virtual_speed:
                    # siamo ancora in accelerazione
                    current_accel = self.accel
                else:
                    # fase di decelerazione
                    current_accel = -self.decel
        else:
            # fase di accelerazione o moto a vel costante
            current_accel = self.accel

        self.virtual_pos += self.virtual_speed * delta_t + \
          0.5 * current_accel * delta_t * delta_t

        self.virtual_speed += current_accel * delta_t

        if self.virtual_speed >= self.vmax:
            self.virtual_speed = self.vmax

        if self.virtual_speed <= 0:
            self.virtual_speed = 0

        vp_x = self.start_x + self.virtual_pos * math.cos(self.target_phi) * math.sin(self.target_theta)
        vp_y = self.start_y + self.virtual_pos * math.sin(self.target_phi) * math.sin(self.target_theta)
        vp_a = self.start_alpha + self.virtual_pos * math.cos(self.target_theta)
        #print(vp_x, vp_y, vp_a, distance)

        (cx, cy, ca) = self.arm.get_pose()

        d = math.sqrt( (cx-self.target_x)**2 + (cy-self.target_y)**2 + (ca-self.target_alpha)**2)

        if d < 1e-2:
            self.target_count += 1
            if self.target_count > 10:
                self.target_got = True
        else:
            self.target_count = 0

        return (vp_x, vp_y, vp_a)

