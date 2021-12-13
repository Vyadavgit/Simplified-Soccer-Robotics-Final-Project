#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.nxtdevices import (LightSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
import random


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

def findBall(sonicSens, right, left):
    # """Find the object by moving the vehicle in multiple directions"""
    # for i in range(18):
    #     rotate(right, left, 20) # 20 degree increments
    #     dist = sonicSens.distance() / 1000
    #     if dist < .45:
    #         # turn to the direction of opponent's base
    #         # keep pushing the ball forward until you hit the opponent's base line color
    #         # bounce back

def wander(colorS, lColorS, sonicS, right, left):
    # boolean = True
    # direction = [0, 90, -90, 180]
    # while(boolean):
    #     rotate(right, left, direction[random.randint(0, 2)])
    #     right.run(360), left.run(360)
    #     while()


# Create your objects here.
def main():
    rightMotor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    leftMotor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    colorSensor = ColorSensor(Port.S4)
    leftColorSensor = ColorSensor(Port.S2)
    sonicSensor = UltrasonicSensor(Port.S1)
    # Write your program here.
    ev3.speaker.beep()
    wander(colorSensor, leftColorSensor, sonicSensor, rightMotor, leftMotor) # wander to search the ball
main()

