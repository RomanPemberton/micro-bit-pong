# Imports go at the top
from microbit import *
import radio
import time
import random

radio.config(group=7)
radio.on()
ball_speed = 1000

# Class for the bouncing ball
class Ball:
    def __init__(self, start_loc, start_dir):
        self.ball_loc = start_loc
        self.ball_dir = start_dir
        self.bounds = [-1, 4, 0, 4]
        self.moving = True

    def move(self, paddle):
        if not (self.bounds[0] <= self.ball_loc[0] + self.ball_dir[0] <= self.bounds[1]):
            self.ball_dir[0] *= -1
        self.ball_loc[0] += self.ball_dir[0]
            
        if not (self.bounds[2] <= self.ball_loc[1] + self.ball_dir[1] <= self.bounds[3]):
            self.ball_dir[1] *= -1
        self.ball_loc[1] += self.ball_dir[1]

        if self.ball_loc[0] == 4:
            if self.ball_loc[1] in paddle.get_loc():
                self.ball_dir[0] *= -1
                self.ball_loc[0] += self.ball_dir[0] * 2
                global ball_speed
                ball_speed *= 0.95
                
            else:
                display.scroll('Loser!')

        elif self.ball_loc[0] == -1:
            if self.ball_dir[0] == -1:
                self.ball_dir[0] = 0
            if self.ball_dir[1] == -1:
                self.ball_dir[1] = 0
            radio.send(str(self.ball_loc[1]) + str(self.ball_dir[0]) + str(self.ball_dir[1]))
            self.moving = False

    def get_loc(self, index):
        return self.ball_loc[index]

    def start_moving(self):
        self.moving = True

    def is_moving(self):
        return self.moving

class Paddle:
    def __init__(self, start_loc, speed):
        self.paddle_loc = start_loc
        self.speed = speed
        self.bounds = [0, 4]

    def move(self, dir):
        if self.bounds[0] <= self.paddle_loc + self.speed * dir <= self.bounds[1] - 1:
            self.paddle_loc += self.speed * dir

    def get_loc(self):
        return [self.paddle_loc, self.paddle_loc + 1]

def refresh_screen():
    display.clear()
    if ball.is_moving():
        display.set_pixel(ball.get_loc(0), ball.get_loc(1), 9)
    display.set_pixel(4, paddle.get_loc()[0], 9)
    display.set_pixel(4, paddle.get_loc()[1], 9)
    

ball = Ball([1, random.randint(0, 4)], [1, 1])
paddle = Paddle(2, 1)
button_down = False
# Code in a 'while True:' loop repeats forever
previous_ms = time.ticks_ms()
while True:
    
    message = radio.receive()
    if message:
        if message[1] == 0:
            ball.ball_dir[0] = -1
        else:
            ball.ball_dir[0] = 1
        if message[2] == 0:
            ball.ball_dir[1] = -1
        else:
            ball.ball_dir[1] = 1
        ball.ball_loc[0] = 0
        ball.ball_loc[1] = int(message[0])
        ball.moving = True
        previous_ms = time.ticks_ms()
        ball_speed *= 0.95

    if not (button_a.is_pressed() or button_b.is_pressed()):
        button_down = False
    
    if button_a.is_pressed() and not button_down:
        paddle.move(-1)
        button_down = True
    
    if button_b.is_pressed() and not button_down:
        paddle.move(1)
        button_down = True
        
    if ball.is_moving():
        current_ms = time.ticks_ms()
        if time.ticks_diff(current_ms, previous_ms) >= ball_speed:
            ball.move(paddle)
            previous_ms = time.ticks_ms()

    refresh_screen()