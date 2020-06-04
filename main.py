#!/usr/bin/python3
import arcade
import os
import time
from PyLSA.PyLSA import *
from graphics import *


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.gridspec as gridspec



class Simulator:
    #   Delta T (simulation time)
    delta_t = 0

    #   CLASSES
    pylsa = None

    def __init__(self, delta_t):
        self.delta_t = delta_t
        self.pylsa = pyLSA()

    def DefineTF(self, Wn, Zeta, K):
        self.pylsa.TransferFunction_Standard(Wn, Zeta, K)  # (1, 0.1, 1)

    def SimulationStepByStep(self, input):
        delta_t = self.delta_t

        # print('IN: ' + str(input))
        # print('AT: ' + str(delta_t))
        response = self.pylsa.LinearSimulationStepByStep(input, delta_t)
        # print('RES: ' + str(int(response)))
        return response

class Physics:
    #   Velocity
    ACCELERATION_MOV = 200
    ACCELERATION_BRK = 100
    VELOCITY_MAX = 100

    #   RAIL
    RAIL_LONG_M = 10
    CABLE_LONG_M = 2

    delta_t = 0.0

    #   trolley
    trolley_velocity = 0.0
    trolley_x = 0.0

    #   key_direction
    key_direction = 0

    def __init__(self, delta_t):
        self.delta_t = delta_t

    def GetCurrentDirectionMovement(self):
        v = self.trolley_velocity
        if v > 0:
            return 1
        elif v < 0:
            return -1
        return 0

    def Right(self):
        delta_t = self.delta_t
        trolley_velocity = self.trolley_velocity
        trolley_x = self.trolley_x
        key_direction = self.GetCurrentDirectionMovement()

        if key_direction == 1 or key_direction == 0:
            if trolley_velocity < self.VELOCITY_MAX:
                trolley_x = float(
                    (trolley_x)
                    + (trolley_velocity * delta_t)
                    + (0.5 * float(self.ACCELERATION_MOV) * (delta_t ** 2.0))
                )
                trolley_velocity = trolley_velocity + (self.ACCELERATION_MOV * delta_t)
                # print("V1: " + str(self.velocity))
            else:
                trolley_x = float((trolley_x) + (trolley_velocity * delta_t))
                trolley_velocity = self.VELOCITY_MAX
                # print("V2: " + str(self.velocity))
        else:
            trolley_x = float(
                (trolley_x)
                + (trolley_velocity * delta_t)
                + (0.5 * float(self.ACCELERATION_MOV) * (delta_t ** 2.0))
                + (0.5 * float(self.ACCELERATION_BRK) * (delta_t ** 2.0))
            )
            trolley_velocity = trolley_velocity + (self.ACCELERATION_BRK * delta_t)
            # print("V3: " + str(self.velocity))

        self.delta_t = delta_t
        self.trolley_x = trolley_x
        self.trolley_velocity = trolley_velocity
        self.key_direction = key_direction

        return trolley_x, trolley_velocity

    def Left(self):
        delta_t = self.delta_t
        trolley_velocity = self.trolley_velocity
        trolley_x = self.trolley_x
        key_direction = self.GetCurrentDirectionMovement()

        if key_direction == -1 or key_direction == 0:
            if trolley_velocity > -self.VELOCITY_MAX:
                trolley_x = float(
                    (trolley_x)
                    + (trolley_velocity * delta_t)
                    - (0.5 * float(self.ACCELERATION_MOV) * (delta_t ** 2.0))
                )
                trolley_velocity = trolley_velocity - (self.ACCELERATION_MOV * delta_t)
                # print("BV1: " + str(self.velocity))
            else:
                trolley_x = float((trolley_x) + (trolley_velocity * delta_t))
                trolley_velocity = -self.VELOCITY_MAX
                # print("BV2: " + str(self.velocity))
        else:
            trolley_x = float(
                (trolley_x)
                + (trolley_velocity * delta_t)
                - (0.5 * float(self.ACCELERATION_MOV) * (delta_t ** 2.0))
                - (0.5 * float(self.ACCELERATION_BRK) * (delta_t ** 2.0))
            )
            trolley_velocity = trolley_velocity - (self.ACCELERATION_BRK * delta_t)
            # print("BV3: " + str(self.velocity))

        self.delta_t = delta_t
        self.trolley_x = trolley_x
        self.trolley_velocity = trolley_velocity
        self.key_direction = key_direction

        return trolley_x, trolley_velocity

    def Middle(self):
        delta_t = self.delta_t
        trolley_velocity = self.trolley_velocity
        trolley_x = self.trolley_x
        key_direction = self.GetCurrentDirectionMovement()

        if key_direction == 1:
            if trolley_velocity < self.VELOCITY_MAX:
                trolley_x = float(
                    (trolley_x)
                    + (trolley_velocity * delta_t)
                    - (0.5 * float(self.ACCELERATION_BRK) * (delta_t ** 2.0))
                )
                trolley_velocity = trolley_velocity - (self.ACCELERATION_BRK * delta_t)
                if trolley_velocity < 0:
                    trolley_velocity = 0
                # print("B- V1: " + str(self.velocity))
            else:
                trolley_x = float((trolley_x) - (trolley_velocity * delta_t))
                trolley_velocity = trolley_velocity - (self.ACCELERATION_BRK * delta_t)
                # print("B- V2: " + str(self.velocity))

        if key_direction == -1:
            if trolley_velocity > -self.VELOCITY_MAX:
                trolley_x = float(
                    (trolley_x)
                    + (trolley_velocity * delta_t)
                    + (0.5 * float(self.ACCELERATION_BRK) * (delta_t ** 2.0))
                )
                trolley_velocity = trolley_velocity + (self.ACCELERATION_BRK * delta_t)
                if trolley_velocity > 0:
                    trolley_velocity = 0
                # print("B- V-1: " + str(self.velocity))
            else:
                trolley_x = float((trolley_x) + (trolley_velocity * delta_t))
                trolley_velocity = trolley_velocity + (self.ACCELERATION_BRK * delta_t)
                # print("B- V-2: " + str(self.velocity))

        self.delta_t = delta_t
        self.trolley_x = trolley_x
        self.trolley_velocity = trolley_velocity
        self.key_direction = key_direction

        return trolley_x, trolley_velocity

class Graphics:
    START_X = 40
    START_Y = 1030

    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0

    trolley = None
    massload = None
    scenario = None

    cable_distance = 0

    def __init__(self, width, height, cable_distance):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.cable_distance = cable_distance

        self.trolley = Trolley(self.START_X)
        self.massload = MassLoad(self.START_X)
        self.masslesscable = MassLessCable(self.START_X, self.START_Y)

    def Draw(self, trolley_x, oscillation_x, oscillation_y):
        Scenario.Draw(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.trolley.Draw(trolley_x, self.START_Y)
        self.massload.Draw(
            oscillation_x, self.START_Y-oscillation_y
        )

        self.masslesscable.Draw(
            trolley_x,
            oscillation_x,
            self.START_Y-oscillation_y
        )
        #print("aa" + str(self.START_Y - (self.START_Y + 2 * 190 - oscillation_y)))

class Trolley:
    start_position = 0

    def __init__(self, start_position):
        self.start_position = start_position

    def Draw(self, trolley_x, trolley_y):
        arcade.draw_rectangle_filled(
            self.start_position + trolley_x, trolley_y, 60, 20, arcade.color.BLUE
        )

class Scenario:
    def Draw(screenWidth, screenHeight):
        arcade.draw_rectangle_filled(
            screenWidth / 2, screenHeight - 75, 1900, 10, arcade.color.BLUE
        )

class MassLoad:
    start_position = 0

    def __init__(self, start_position):
        self.start_position = start_position

    def Draw(self, mass_x, mass_y):
        arcade.draw_circle_filled(
            self.start_position + mass_x, mass_y, 10, arcade.color.RED
        )

class MassLessCable:
    start_x = None
    start_y = None

    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y

    def Draw(self, trolley_x, load_x, load_y):
        arcade.draw_line(
            self.start_x + trolley_x,
            self.start_y,
            self.start_x + load_x,
            load_y,
            arcade.color.RED,
        )

class Maths:
    def CalculateMassLoad_Y(cable_long_m, load_x, trolley_x, trolley_velocity):
        CONVERSION_RATE = 190
        try:
            theta = math.asin((trolley_x - load_x) / (cable_long_m * CONVERSION_RATE))
            if load_x > 0:
                load_y = cable_long_m * CONVERSION_RATE * math.cos(theta)
            else:
                load_y = cable_long_m * CONVERSION_RATE * math.cos(theta)
            return load_y

            print("theta: " + str(theta))
        except:
            print('OverOscilation') 
            return 0

class MyGame(arcade.Window):
    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0

    simulator = None
    graphics = None
    physics = None

    # KEY DIRECTION [-1, 0, 1]
    direction_numeric = 0

    # KEY PRESSED
    left_pressed = None
    right_pressed = None

    RAIL_LONG_M = 10
    CABLE_LONG_M = 2

    DELTA_T = 0.02

    def __init__(self, width, height, title):
        self.direction = 0
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        # Call the parent class initializer
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        arcade.set_background_color(arcade.color.WHITE)

        self.simulator = Simulator(self.DELTA_T)
        self.graphics = Graphics(
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.CABLE_LONG_M
        )
        self.physics = Physics(self.DELTA_T)

    def setup(self):
        self.simulator.DefineTF(2, 0.1, 1)

    def on_draw(self):
        oscillation_x = 0
        arcade.start_render()
        trolley_x, trolley_velocity = self.PHYSICS_GetTrolley_X_V()

        oscillation_x = self.simulator.SimulationStepByStep(trolley_x)
        oscillation_y = Maths.CalculateMassLoad_Y(
            self.CABLE_LONG_M, oscillation_x, trolley_x, trolley_velocity
        )

        # print("oscillation_x: " + str(oscillation_x))
        # print("oscillation_y: " + str(oscillation_y))

        #print(str(oscillation_y))
        self.graphics.Draw(trolley_x, oscillation_x, oscillation_y)




    def on_update(self, delta_time):
        direction_numeric = self.direction_numeric
        if self.left_pressed and not self.right_pressed:
            direction_numeric = -1
        elif self.right_pressed and not self.left_pressed:
            direction_numeric = 1
        elif not self.right_pressed and not self.left_pressed:
            direction_numeric = 0
        self.direction_numeric = direction_numeric

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
            self.right_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.left_pressed = False

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def PHYSICS_GetTrolley_X_V(self):
        direction_numeric = self.direction_numeric
        trolley_x = 0

        if direction_numeric == 1:
            return self.physics.Right()
        elif direction_numeric == 0:
            return self.physics.Middle()
        elif direction_numeric == -1:
            return self.physics.Left()

def main():
    #   SYSTEM METRICS (SCREEN SIZE)
    import subprocess

    cmd = ["xrandr"]
    cmd2 = ["grep", "*"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()
    resolution_string, junk = p2.communicate()
    resolution = resolution_string.split()[0]

    res = str(resolution).split("x")
    ww = int(res[0][2:])
    hh = int(res[1][:-1])
    #   -----------------------------------------

    window = MyGame(ww, hh, "")
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
