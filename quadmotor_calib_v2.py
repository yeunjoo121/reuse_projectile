import RPi.GPIO as GPIO
import pigpio
import time

#GPIO.setmode(GPIO.BOARD)
pi = pigpio.pi()

motorA_pin = 27;#GPIO27 - pin13 아래  
motorB_pin = 22;#GPIO22 - pin15 위 
#motorC_pin = 17;#GPIO4 - pin7
goal_pwm = 1400
goal_delay = 40

ESC_PWM_MIN = 1150
ESC_PWM_START = 1200
ESC_PWM_MAX = 1800

# ESC_PWM_MIN = 1450
# ESC_PWM_START = 1500
# ESC_PWM_MAX = 2000


print("connect ok")
try:
    for i in range(120):
        if ((1200 + 5 * i) == goal_pwm):
            ti = goal_delay;
        else:
            ti = 0.1;
        
        print(i)
        print(ESC_PWM_START + i*5)
        pi.set_servo_pulsewidth(motorA_pin,1200+5*i) #아래 
        #pi.set_servo_pulsewidth(motorB_pin, i*50+ ESC_PWM_MIN)
        pi.set_servo_pulsewidth(motorB_pin,1300) #위 
        #pi.set_servo_pulsewidth(motorA_pin, i*50 + ESC_PWM_MIN) 
        time.sleep(float(ti))
            

    #stop
    pi.set_servo_pulsewidth(motorA_pin, ESC_PWM_MIN)
    pi.set_servo_pulsewidth(motorB_pin, ESC_PWM_MIN)
    #pi.set_servo_pulsewidth(motorC_pin, ESC_PWM_MIN)

except KeyboardInterrupt:
    pi.set_servo_pulsewidth(motorA_pin, ESC_PWM_MIN)
    pi.set_servo_pulsewidth(motorB_pin, ESC_PWM_MIN)
    