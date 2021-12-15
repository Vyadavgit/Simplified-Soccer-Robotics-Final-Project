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

def rotate(right, left, angle, gyroSensor, velocity = 150):
    while gyroSensor.angle() != angle:
        if(gyroSensor.angle() < angle):
            # if its less than 0 turn right
            right.run(-velocity)
            left.run(velocity)
        else:
            # if its more than 0 turn left
            right.run(velocity)
            left.run(-velocity)
    else: 
        right.stop()
        left.stop()
        return

def goToHome(colorSensor, gyroSensor, right, left):
    ev3.screen.print("Going Home")
    goToTarget(right, left, -.1)
    rotate(right, left, 180, gyroSensor)
    time.sleep(.25)
    while colorSensor[0].color() != Color.RED:
        right.run(500)
        left.run(500)
    else:
        right.stop()
        left.stop()
        goToTarget(right, left, .3)
        rotate(right, left, 0, gyroSensor)
        gyroSensor.reset_angle(0)
        return

def score(gyroSensor, colorSensor, irSensor, right, left):
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
        right.stop()
        left.stop()
        while colorSensor[0].color() != Color.BLUE and colorSensor[1].color() != Color.BLUE:
            right.run(1000)
            left.run(1000)
            if max(irSensor.get_strength()) < 10:
                right.stop()
                left.stop()
                return False
        else:
            right.stop()
            left.stop()
            goToHome(colorSensor, gyroSensor, right, left)
            return True


def align(irSensor, colorSensors, right, left):
    ev3.screen.print("Aligning")
    zones = [5]
    if max(irSensor.get_strength()) < 5:
        right.run(360)
        left.run(360)
        while max(irSensor.get_strength()) < 5:
            if colorSensors[0].color() == Color.BLUE or colorSensors[1].color() == Color.BLUE:
                right.stop()
                left.stop()
                return False
            continue
    right.stop()
    left.stop()
    while irSensor.get_zone() not in zones: 
        if(irSensor.get_zone() < 5):
            # if its less than 5 its on its left 
            right.run(360)
            left.run(-360)
        else: 
            # if its more than 5 its on the right
            right.run(-360)
            left.run(360)
    right.stop()
    left.stop()
    return True

def ballFollow(irSensor, colorSensor, gyroSensor, right, left):
    ev3.screen.print("Following Ball")
    while irSensor.get_strength()[2] < 30 and irSensor.get_strength()[1] < 30 and irSensor.get_strength()[3] < 30: 
        if(colorSensor[0].color() == Color.BLUE or colorSensor[1].color() == Color.BLUE):
            goToHome(colorSensor, gyroSensor, right, left)
            return False
        right.run(500)
        left.run(500)
    else:
        right.stop()
        left.stop()
        return True


# Create your objects here.
def main():
    rightMotor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    leftMotor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    colorSensor = ColorSensor(Port.S3)
    leftColorSensor = ColorSensor(Port.S4)
    gyroSensor = GyroSensor(Port.S1)
    irSensor = InfraredSensor(Port.S2)

    # Write your program here.
    ev3.speaker.beep()
    if align(irSensor, (colorSensor, leftColorSensor), rightMotor, leftMotor):
        if ballFollow(irSensor, (colorSensor, leftColorSensor), gyroSensor, rightMotor, leftMotor):
            score(gyroSensor, (colorSensor, leftColorSensor), irSensor, rightMotor, leftMotor)
    else: 
        goToHome((colorSensor, leftColorSensor), gyroSensor, rightMotor, leftMotor)
    while True:
        if irSensor.get_zone():
            if align(irSensor, (colorSensor, leftColorSensor), rightMotor, leftMotor):
                if ballFollow(irSensor, (colorSensor, leftColorSensor), gyroSensor, rightMotor, leftMotor):
                    score(gyroSensor, (colorSensor, leftColorSensor), irSensor, rightMotor, leftMotor)
            else: 
                goToHome((colorSensor, leftColorSensor), gyroSensor, rightMotor, leftMotor)
        else: 
            continue


main()