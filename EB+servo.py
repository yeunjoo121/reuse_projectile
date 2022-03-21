import serial
import time
import RPi.GPIO as GPIO  # 라즈베리파이 GPIO관련 모듈을 불러옴 
from time import sleep

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
servo_max_duty = 12 # 최대 듀티비를 12로

def set_servo_degree_Roll (servo_num, degree1): # 각도를 입력하면 듀티비를 알아서 설정해주는 함수
                                          # 각도는 최소 0, 최대 180으로 설정
    if degree1 >= 0 :
        degree1 = (degree1+180)/2
    elif degree1 < 0 :
        degree1 = (degree1+180)/2
        
    # 입력한 각도를 듀티비로 환산하는 식
    duty = servo_min_duty + (degree1*(servo_max_duty - servo_min_duty)/180.0)
    # 환산한 듀티비를 서보모터에 전달
    if servo_num == 1:
        servo1.ChangeDutyCycle(duty)
    elif servo_num == 2:
        servo2.ChangeDutyCycle(duty)

def set_servo_degree_Pitch (servo_num, degree2): # 각도를 입력하면 듀티비를 알아서 설정해주는 함수
                                          # 각도는 최소 0, 최대 180으로 설정
    if degree2 >= 0 :
        degree2 = (degree2+90)
    elif degree2 < 0 :
        degree2 = (degree2+90)
        
        
    # 입력한 각도를 듀티비로 환산하는 식
    duty = servo_min_duty + (degree2*(servo_max_duty - servo_min_duty)/180.0)
    # 환산한 듀티비를 서보모터에 전달
    if servo_num == 1:
        servo1.ChangeDutyCycle(duty)
    elif servo_num == 2:
        servo2.ChangeDutyCycle(duty)
        
EBIMU = serial.Serial('/dev/ttyUSB0',115200) # baudrate = 115200 = <sb5>
# EBIMU.write(b'<lf>') # b는 binary, <lf>는 초기값 load
EBIMU.write(b'<sor0>') # <sor0>는 polling mode (set output rate)
EBIMU.write(b'<sof1>') # <sof1>는 Euler Angles 출력
EBIMU.write(b'<sog1>') # <sog1>은 자이로(각속도) 데이터 출력
EBIMU.write(b'<soa1>') # <soa1>는 가속도 데이터 출력 

time.sleep(.3)
EBIMU.flushInput() # flushInout은 캐시에 받은 모든 데이터 폐기

Hz = 100
dt = 1/Hz
time_old = 0

while True:
    while time_old + dt > time.time(): # 이 조건이 없으면 time_now - time_old 가 0에 수렴한다 
        time.sleep(dt*0.01)
    time_now = time.time()
    freq = 1/(time_now - time_old)
    time_old = time_now
    #print(freq)
    
    # sensor data
    for i in range(1):
        EBIMU.write(b'*')
        s = EBIMU.read(1)
        if s == b'*':
            data = b''
            while s != b'\n':
                s = EBIMU.read(1)
                data = data + s
            data = data[0:len(data)-2]
            transmitted_string = data.decode('utf-8')
            splited_string = transmitted_string.split(',')
            Roll = float(splited_string[0]) # -180 ~ +180도, float는 값을 실수형 자료로 변경
            Pitch = float(splited_string[1]) # -90 ~ +90도
            Yaw = float(splited_string[2]) # -180 ~ +180도
            Gyro_X = float(splited_string[3]) # 자이로 데이터의 단위는 DPS(degree per second)
            Gyro_Y = float(splited_string[4])
            Gyro_Z = float(splited_string[5])
            X_acc = float(splited_string[6]) # 가속도의 단위는 중력가속도 g, g = 9.81m/s^2
            Y_acc = float(splited_string[7])
            Z_acc = float(splited_string[8])
            
            
            print("Roll : {0} Pitch : {1} Yaw : {2}".format(Roll, Pitch, Yaw))
            print("Gyro_X : {0} Gyro_Y : {1} Gyro_Z : {2}".format(Gyro_X, Gyro_Y, Gyro_Z))
            print("X_acc : {0} Y_acc : {1} Z_acc : {2}".format(X_acc, Y_acc, Z_acc))
            set_servo_degree_Roll(1, Roll)
            set_servo_degree_Pitch(2, Pitch)
            sleep(0.01)
           
            
EBIMU.close()
GPIO.cleanup()