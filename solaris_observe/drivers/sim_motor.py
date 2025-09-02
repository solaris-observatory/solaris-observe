"""
Simulator motor driver.
"""

from .base import MotorDriver

class SimMotor(MotorDriver):
    def __init__(self):
        self.trace = []
    def enable(self):
        self.trace.append(("enable",))
    def set_velocity(self, az, el):
        self.trace.append(("set_velocity", az, el))
    def move_abs(self, az, el):
        self.trace.append(("move_abs", az, el))
    def stop(self):
        self.trace.append(("stop",))
