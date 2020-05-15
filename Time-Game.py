
import RPi.GPIO as GPIO
import time
import random
import sys

RUNNING = True
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pin = 19
servoangle = 90
LED_R = 2
LED_G = 3

A_RED = 17
A_GREEN = 27
B_RED = 23
B_GREEN = 22

Round = 0
APoints = 0
BPoints = 0
color = ""
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(A_RED, GPIO.IN)
GPIO.setup(A_GREEN, GPIO.IN)
GPIO.setup(B_RED, GPIO.IN)
GPIO.setup(B_GREEN, GPIO.IN)

pwm = GPIO.PWM(pin,50)
pwm.start(0)

print("Starting Game...")

#Servo
def SetAngle(angle):
    duty = angle/18+2
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)

SetAngle(90)
time.sleep(1)

def newColor():
    global color
    GPIO.output(LED_R, False)
    GPIO.output(LED_G, False)
    time.sleep(0.2)
    GPIO.output(LED_R, True)
    GPIO.output(LED_G, True)
    print("...")
    time.sleep(0.5)
    r = random.choice([0,1])
    if (r == 1):
        GPIO.output(LED_R, True)
        GPIO.output(LED_G, False)
        color = "Red"
        print("RED!")
    elif (r == 0):
        GPIO.output(LED_R, False)
        GPIO.output(LED_G, True)
        color = "Green"
        print("GREEN!")

def score(x):
    global servoangle
    global APoints
    global BPoints
    global SetAngle
    if (x == "A"):
       servoangle = servoangle + 25
       APoints = APoints + 1
       GPIO.output(LED_G, False)
       GPIO.output(LED_R, False)
       SetAngle(servoangle)
       print("Player A gets a point!")
    if (x == "B"):
        servoangle = servoangle - 25
        BPoints = BPoints + 1
        GPIO.output(LED_G, False)
        GPIO.output(LED_R, False)
        SetAngle(servoangle)
        print("Player B gets a point!")

#start game
while(Round < 4):
    print("Round: ", Round + 1)

    newColor()
    time.sleep(1)
    Round = Round + 1

    if ((GPIO.input(A_RED) == False) and (color == "Red")):
        print("Player A got it!")
        score("A")
        time.sleep(2)
    elif ((GPIO.input(B_RED) == False) and (color == "Red")):
        print("Player B got it!")
        score("B")
        time.sleep(2)
    elif ((GPIO.input(B_RED) == True) and (GPIO.input(B_RED) == True) and (color == "Red")):
        print("It's a Draw!")

    if ((GPIO.input(A_GREEN) == False) and (color == "Green")):
        print("Player A got it!")
        score("A")
        time.sleep(2)
    elif ((GPIO.input(B_GREEN) == False) and (color == "Green")):
        print("Player B got it!")
        score("B")
        time.sleep(2)
    elif ((GPIO.input(A_GREEN) == True) and (GPIO.input(B_GREEN) == True) and (color == "Green")):
        print("It's a Draw!")

if (Round == 4):
    GPIO.output(LED_R, True)
    GPIO.output(LED_G, True)
    print("Final Score:\n")
    print("Player A: ", APoints)
    print("Player B: ", BPoints)