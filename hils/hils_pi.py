import RPi.GPIO as GPIO
import pigpio
import serial
import time
import numpy as np
import math

#----------------------------------------#
#-----------add code for hils------------#
port0 = '/dev/ttyAMA0'
port3 = '/dev/ttyAMA1'
baud = 115200

# ser0 -> send * and receive sensor data
# ser3 -> send angle or rpm
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

star = '*'
null = '\0'
#---------------------------------------#

np.set_printoptions(precision=6, suppress = True)

pi = pigpio.pi()

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
                #self.transmitted[j] = float(splited_str[j])
                self.transmitted[j] = 1
                
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
    global star
    global null
    buffer1 = ([[0, 0, 0, 0, 0, 0, 0, 0, 0]])

    print("start")
    
    data = Data()
    
    # there is no need to set EBIMU
    
    while (True):
        # print('star write')
        ser0.write(star.encode()); # *하나 써서 데이터 받아오기 시작
        s = ser0.read().decode()# 데이터 하나씩 읽어옴
        if (s == '*'):
            datainput = ''
            while (s != '\n'):
                s = ser0.read().decode()
                datainput = datainput + s
                
            print('receive data=' + datainput)
            
            # 여기서 연산
            datainput = datainput[0:len(datainput) - 2] # \r\n제거
            print(datainput)
            splited_str = datainput.split(',')

            data.str_to_float(splited_str)
            
            data.print_data()
            buffer1 = np.append(buffer1, data.get_data(), axis = 0) # data 저장
            
            # pwm값 desktop으로 보내기 & pwm 연산
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
            
            # no need to move servo
            #pi.set_servo_pulsewidth(7, a)
            #pi.set_servo_pulsewidth(12, a)
                
            # send angle or rpm
            element = 1/7
            msg = str(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + '\n'
            ser3.write(msg.encode())
            print(type(data.Roll))
            print(type(element))

main()