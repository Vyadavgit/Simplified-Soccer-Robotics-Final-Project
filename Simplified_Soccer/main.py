#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                    UltrasonicSensor, GyroSensor)
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
import random

# Create InfraredSensor class
class InfraredSensor():
    def __init__(self, port):
        self.sensor = I2CDevice(port, 0x01)
    
    def get_zone(self):
        """Returns Zone that IR signal is observed in."""
        return int.from_bytes(self.sensor.read(0x42, length=1), "little")
    
    def get_strength(self): 
        """Returns an array with the relative strength of IR in each zone."""
        retArray = []
        for i in range(5):
            strength = int.from_bytes(self.sensor.read(0x43+i, length=1), "little")
            retArray.append(strength)
        return retArray
        

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
wheelCirc = (5.3975*3.14159)/100 # meters
robotCirc = (12.065*3.14159)/100 # meters
wallColor = 10
ev3 = EV3Brick()

def goToTarget(right, left, target, velocity = 360):
    resetAngles(right, left)
    desired_angle = (target/wheelCirc)*360
    right.run_angle(velocity, desired_angle, Stop.HOLD, False)
    left.run_angle(velocity, desired_angle)

def resetAngles(right, left, angle = 0):
    right.reset_angle(angle)
    left.reset_angle(angle)

def rotate(right, left, angle=90, velocity = 150):
    ratio = angle/360
    dist = robotCirc * ratio
    desiredAngle = ((dist/wheelCirc) * 360 * (14/15))
    resetAngles(right, left)
    right.run_target(velocity, desiredAngle, Stop.HOLD, False)
    left.run_target(velocity, -desiredAngle)

def score(gyroSensor, right, left):
    ev3.screen.print("scoring")
    while(gyroSensor.angle() < -5 or gyroSensor.angle() > 5):
        if(gyroSensor.angle() < 0):
            # if its less than 0 turn right
            right.run(-160)
            left.run(160)
        else:
            # if its more than 0 turn left
            right.run(160)
            left.run(-160)
    else:
        goToTarget(right, left, .3, 500)


def align(irSensor, right, left):
    ev3.screen.print("aligning")
    zones = [4, 5, 6]
    while irSensor.get_zone() not in zones: 
        if(irSensor.get_zone() < 5):
            # if its less than 5 its on its left 
            right.run(160)
            left.run(-160)
        else: 
            # if its more than 5 its on the right
            right.run(-160)
            left.run(160)
    right.stop()
    left.stop()
    return True

def ballFollow(irSensor, right, left):
    ev3.screen.print("ballFollow")
    if align(irSensor, right, left):
        while irSensor.get_strength()[2] < 40 or irSensor.get_strength()[1] < 40: 
            right.run(160)
            left.run(160)
        else:
            right.stop()
            left.stop()
            return "score"


# Create your objects here.
def main():
    rightMotor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    leftMotor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    colorSensor = ColorSensor(Port.S3)
    leftColorSensor = ColorSensor(Port.S4)
    gyroSensor = GyroSensor(Port.S1)
    irSensor = InfraredSensor(Port.S2)
    # direction info 0x42 
    # 0x43 strength at 5 ir segments
    # read separately 
    # Write your program here.
    ev3.speaker.beep()
    # if ballFollow(irSensor, rightMotor, leftMotor) == "score":
    #     score(gyroSensor, rightMotor, leftMotor)
    while True: 
        print(irSensor.get_strength())
        time.sleep(1)
main()

