from subprocess import call
call("sudo pigpiod", shell=True)
import RPi.GPIO as GPIO
import pigpio
import time

GPIO.setmode(GPIO.BOARD)
pi = pigpio.pi()

motorA_pin = 22;
motorB_pin = 27;
motorC_pin = 4;

ESC_PWM_MIN = 1050
ESC_PWM_MAX = 1350

for i in range(10):
    pi.set_servo_pulsewidth(motorA_pin, i * 30 + ESC_PWM_MIN)

pi.set_servo_pulsewidth(motorA_pin, ESC_PWM_MAX)