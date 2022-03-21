import RPi.GPIO as GPIO  # 라즈베리파이 GPIO관련 모듈을 불러옴 
from time import sleep   # time 라이브러리의 sleep 함수 사용

GPIO.setwarnings(False) # RuntimeWarning : This channel is already use 문제 해결하기 위해서
GPIO.setmode(GPIO.BCM) # Broadcom SoC 칩에서 사용하는 핀 번호를 사용함

servo1_pin = 12 # 서보1 핀은 라즈베리파이 GPIO 12번핀으로 설정
servo2_pin = 7  # 서보2 핀은 라즈베리파이 GPIO 7번 핀으로 설정 

GPIO.setup(servo1_pin, GPIO.OUT) # 서보1 핀을 출력으로 설정
GPIO.setup(servo2_pin, GPIO.OUT) # 서보2 핀을 출력으로 설정

servo1 = GPIO.PWM(servo1_pin, 50) # 서보핀을 PWM모드 50Hz로 사용
servo2 = GPIO.PWM(servo2_pin, 50) # 서보핀을 PWM모드 50Hz로 사용

servo1.start(0) # 서보1의 초기값을 0으로 설정
servo2.start(0) # 서보2의 초기값을 0으로 설정

servo_min_duty = 3 # 최소 듀티비를 3으로
servo_max_duty = 18 # 최대 듀티비를 12로

def set_servo_degree (servo_num, degree): # 각도를 입력하면 듀티비를 알아서 설정해주는 함수
                                          # 각도는 최소 0, 최대 180으로 설정
    if degree > 0 :
        degree = degree
    elif degree < 0 :
        degree = degree
        
    # 입력한 각도를 듀티비로 환산하는 식
    duty = servo_min_duty + (degree*(servo_max_duty - servo_min_duty)/180.0)
    # 환산한 듀티비를 서보모터에 전달
    if servo_num == 1:
        servo1.ChangeDutyCycle(duty)
    elif servo_num == 2:
        servo2.ChangeDutyCycle(duty)

try :
    while True:
        for roll in range(0, 180, 1): # 서보1은 roll값에 -를 붙여서 제어 예정
            set_servo_degree(1, 75)
            set_servo_degree(2, 75)
            sleep(0.01)
#         for pitch in range(40  , 120, 10): # 서보2는 pitch값에 -를 붙여서 제어 예정
#             set_servo_degree(2, pitch)
        

finally :                    # try구문이 종료되면
    GPIO.cleanup()           # GPIO 핀들을 초기화
                            
