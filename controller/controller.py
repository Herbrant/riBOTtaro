import websocket
import sys
import math
import time
import json
from pathlib import Path

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../")

from lib.phidias.phidias_interface import start_message_server_http, Messaging
from lib.controllers.control2d import Polar2DController, Path2D
from lib.controllers.standard import PIDSat
from lib.models.robot import RoboticSystem
from lib.models.cart2d import TwoWheelsCart2DEncodersOdometry

class Cart2DRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3)  # delta_t = 1e-3
        # Mass = 1kg
        # radius = 15cm
        # friction = 0.8

        self.cart = TwoWheelsCart2DEncodersOdometry(20, 0.15, 0.8, 0.8,
                                                    0.025, 0.025, 0.2,
                                                    0.02, 0.02, 0.24, 2*math.pi/4000.0)
        
        # 5 Nm of max torque, antiwindup
        self.left_controller = PIDSat(2.0, 2.0, 0.0, 5, True)
        self.right_controller = PIDSat(2.0, 2.0, 0.0, 5, True)

        # Path controller
        self.polar_controller = Polar2DController(1, 0.5, 1.5, 2)
        self.path_controller = Path2D(0.5, 0.2, 0.2, 0.02)  # tolerance 1cm
        self.path_controller.set_path([(0, 0)])
        (x, y, _) = self.get_pose()
        self.path_controller.start((x, y))
        self.target_reached = False
        
        # Networking
        self.phidias_agent = ''
        self.http_server_thread = start_message_server_http(self)
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://127.0.0.1:8000")

    def run(self):
        while True:
            pose = self.get_pose()
            target = self.path_controller.evaluate(self.delta_t, pose)
            
            if target is not None:
                print("Target: ", target) 
            if target is not None: 
                print("Target: ", target) 
                self.ws.send(json.dumps(pose))
                
                # polar control
                (v_target, w_target) = self.polar_controller.evaluate(self.delta_t, target[0], target[1], pose)
                vref_l = v_target - w_target * self.cart.encoder_wheelbase / 2.0
                vref_r = v_target + w_target * self.cart.encoder_wheelbase / 2.0
                
                (vl, vr) = self.cart.get_wheel_speed()
                # speed control (left, right)
                Tleft = self.left_controller.evaluate(self.delta_t, vref_l, vl)
                Tright = self.right_controller.evaluate(self.delta_t, vref_r, vr)
                
                # robot model
                self.cart.evaluate(self.delta_t, Tleft, Tright)
            else:
                if not self.target_reached:
                    self.target_reached = True
                    if self.phidias_agent != '':
                        print("Target")
                        Messaging.send_belief(self.phidias_agent, 'target_reached', [], 'robot')
                
            time.sleep(1e-3);   
        #return True     

    def get_pose(self):
        return self.cart.get_pose()

    def get_speed(self):
        return self.cart.get_speed()

    def on_belief(self, _from, name, terms):
        print(_from, name, terms)
        self.phidias_agent = _from
        
        if name == 'go_to':
            self.target_reached = False
            self.path_controller.set_path([(terms[0], terms[1])])
            (x, y, _) = self.get_pose()
            self.path_controller.start((x, y))


if __name__ == '__main__':
    cart_robot = Cart2DRobot()
    cart_robot.run() 

