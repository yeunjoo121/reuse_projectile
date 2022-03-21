from subprocess import call
call("sudo pigpiod", shell=True)
import RPi.GPIO as GPIO
import pigpio
import time
