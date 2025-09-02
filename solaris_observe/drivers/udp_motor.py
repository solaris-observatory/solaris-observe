"""
UDP motor driver (stub).
"""

from .base import MotorDriver

class UDPMotor(MotorDriver):
    def __init__(self, ip: str, port: int):
        self.ip, self.port = ip, port
    def enable(self):
        print(f"[UDP] enable at {self.ip}:{self.port}")
    def set_velocity(self, az, el):
        print(f"[UDP] set_velocity az={az}, el={el}")
    def move_abs(self, az, el):
        print(f"[UDP] move_abs az={az}, el={el}")
    def stop(self):
        print("[UDP] stop")
