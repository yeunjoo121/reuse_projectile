import RPi.GPIO as GPIO
import pigpio
import time

#GPIO.setmode(GPIO.BOARD)
pi = pigpio.pi()

motorA_pin = 27;#GPIO27 - pin13
motorB_pin = 22;#GPIO22 - pin15
#motorC_pin = 17;#GPIO4 - pin7

ESC_PWM_MIN = 1050
ESC_PWM_MAX = 1350

print("connect ok")

for i in range(10):
    print(ESC_PWM_MIN + i * 30)
    pi.set_servo_pulsewidth(motorA_pin, i * 30 + ESC_PWM_MIN)
    pi.set_servo_pulsewidth(motorB_pin, i * 30 + ESC_PWM_MIN)
    #pi.set_servo_pulsewidth(motorC_pin, i * 30 + ESC_PWM_MIN)
    time.sleep(1)

#stop
pi.set_servo_pulsewidth(motorA_pin, ESC_PWM_MIN)
pi.set_servo_pulsewidth(motorB_pin, ESC_PWM_MIN)
#pi.set_servo_pulsewidth(motorC_pin, ESC_PWM_MIN)