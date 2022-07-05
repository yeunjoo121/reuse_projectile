import serial
import time
import RPi.GPIO as GPIO
import pigpio
import serial
import numpy as np
import math


port0 = '/dev/ttyS0'
part3 = 'dev/ttyAMA1'
baud = 115200

ser0 = serial.Serial(
    port = port0,
    baudrate = baud,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 5
    )

ser3 = serial.Serial(
    port = port3,
    baudrate = baud,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 5
    )

line = ''
star = '*'
pi = pigpio.pi()
np.set_printoptions(precision=6, suppress = True)

class Data:
    # transmitted의 첫번째는 sensor 값 받아오는 것, 두번째는 process하는 것, 세번째는 
    transmitted = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    Roll = 0.0
    Pitch = 0.0
    Yaw = 0.0
    Gyro_X = 0.0
    Gyro_Y = 0.0
    Gyro_Z = 0.0
    X_acc = 0.0
    Y_acc = 0.0
    Z_acc = 0.0
        
    #0부터 9, '.', '-'이외의 값 들어오면 이전값으로 계속 있음. 정해진 값 들어와야 바꿈.
    def str_to_float(self, splited_str): 
        for j in range(0, 9):# transmitted에 다 넣고 나중에 분리
            error = 0
            for i in range(0, len(splited_str[j])):
                if (not((splited_str[j][i] >= '0' and splited_str[j][i] <= '9') or (splited_str[j][i] == '.')
                      or (splited_str[j][i] == '-'))):
                   
                    error = 1
            if (error == 0):
                self.transmitted[j] = float(splited_str[j])
                
        self.Roll = self.transmitted[0]
        self.Pitch = self.transmitted[1]
        self.Yaw = self.transmitted[2]
        self.Gyro_X = self.transmitted[3]
        self.Gyro_Y = self.transmitted[4]
        self.Gyro_Z = self.transmitted[5]
        self.X_acc = self.transmitted[6]
        self.Y_acc = self.transmitted[7]
        self.Z_acc = self.transmitted[8]

    
    # data 출력하는 함수
    def print_data(self):
        print("Roll : {0} Pitch : {1} Yaw : {2}".format(self.Roll, self.Pitch, self.Yaw))
        print("Gyro_X : {0} Gyro_Y : {1} Gyro_Z : {2}".format(self.Gyro_X, self.Gyro_Y, self.Gyro_Z))
        print("X_acc : {0} Y_acc : {1} Z_acc : {2}".format(self.X_acc, self.Y_acc, self.Z_acc))
        print("\n")
        
    def get_data(self):
        arr = np.array([[self.Roll, self.Pitch, self.Yaw, self.Gyro_X, self.Gyro_Y, self.Gyro_Z,
                        self.X_acc, self.Y_acc, self.Z_acc]])
        return arr
    
    
def main():
    global line
    global star
    buffer1 = ([[0, 0, 0, 0, 0, 0, 0, 0, 0]])

    print("pi ready")
    
    data = Data()
    
    while (True):
        print('star write')
        ser.write(star.encode());
        ch = ser.read().decode()
        if (ch == '*'):
            line = ''
            while (not line.endswith('\n')):
                line += ser.read().decode()
                
            print('receive data=' + line)
            
            # 여기서 연산
            temp = line[1:len(line) - 2] # *,\y\n제거
            splited_str = temp.split(',')

            data.str_to_float(splited_str)
            
            data.print_data()
            buffer1 = np.append(buffer1, data.get_data(), axis = 0) # data 저장
            
            # pwm값 desktop(matlab)으로 보내기 & pwm 연산
            a = 1500-(100/9*(data.Yaw))
            b = 1334+(50*(data.Pitch)/9)
            if (a <= 500):
                a = 500
            elif (a >= 2500):
                a = 2500
                
            if (b <= 500):
                b = 500
            elif (b >= 2500):
                b = 2500
            
            #pi.set_servo_pulsewidth(7, a)
            #pi.set_servo_pulsewidth(12, a)
                
            # 여기서 a값은 voltage로 변환이 필요!!
            voltage = a/400 - 1.25
            ser.write(('[' + str(voltage) + ']').encode())
            
            # line reset
            line = ''

main()