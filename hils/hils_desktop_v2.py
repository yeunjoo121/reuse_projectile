import time
import serial
import random
import numpy as np

port5 = 'COM5' # port for receive * and send sensor data
port6 = 'COM6' # port for receive rpm or angle from raspberry pi

baud = 115200

ser5 = serial.Serial(
    port = port5,
    baudrate = baud,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 5
    )

ser6 = serial.Serial(
    port = port6,
    baudrate = baud,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 5
    )

class Data:
    transmitted = [0.0, 0.0, 0.0, 0.0]
    rpm1 = 0.0
    rpm2 = 0.0
    angle1 = 0.0
    angle2 = 0.0

    def str_to_float(self, splited_str):
        if (len(splited_str) == 4):#4이면 숫자나 -, .가 아닌 값이 들어간 데이터를 nan 처리
            for j in range(0, 4):
                error = 0
                decimalP = 0
                minus = 0
                for i in range(0, len(splited_str[j])):
                    if (not((splited_str[j][i] >= '0' and splited_str[j][i] <= '9') or (splited_str[j][i] == '.')
                          or (splited_str[j][i] == '-'))):
                        error = 1
                    if (splited_str[j][i] == '.'):
                        decimalP += 1
                        if (decimalP >= 2):
                            error = 1
                    elif (splited_str[j][i] == '-'):
                        minus += 1
                        if (minus >= 2):
                            error = 1
                if (error == 0):
                    self.transmitted[j] = float(splited_str[j])
                elif (error == 1):
                    self.transmitted[j] = np.NaN
        elif (len(splited_str) > 4): # len이 4보다 크면 숫자값 또는 '.', '-'가 ','로 처리된 것이라 어떤 숫자가 ,로 잘못 들어간 것인지 모르므로 전체 data를 nan처리
            for j in range (0, 4):
                self.transmitted[j] = np.NaN
        elif (len(splited_str) < 4): #len이 4보다 작으면 maxlen과 비교
            index = 0
            for j in range(0, len(splited_str)):
                error = 0
                decimalP = 0
                minus = 0
                for i in range(0, len(splited_str[j])):
                    if (i >= 10):# maxlen보다 크면 이 데이터와 다음 데이터 nan처리
                        error = 2
                        break
                    if (not((splited_str[j][i] >= '0' and splited_str[j][i] <= '9') or (splited_str[j][i] == '.')
                      or (splited_str[j][i] == '-'))):
                        error = 1
                    if (splited_str[j][i] == '.'):
                        decimalP += 1
                        if (decimalP >= 2):
                            error = 2
                    elif (splited_str[j][i] == '-'):
                        minus += 1
                        if (minus >= 2):
                            error = 2
                if (error == 0):
                    self.transmitted[index] = float(splited_str[j])
                    index += 1
                elif (error == 1):# filtering 단계에서 바꾸어줌. 센서들로 추측값을 넣던지, 혹은 이전 값을 넣던지.
                    self.transmitted[index] = np.NaN
                    index += 1
                elif (error == 2):# 이번 값과 다음 값을 모두 nan으로 처리해줌. ','가 손실되어 이번 값과 다음 값을 구분해 주는 ,가 없으므로 j를 1 증가시킨다.
                    self.transmitted[index] = np.NaN
                    index += 1
                    self.transmitted[index] = np.NaN
                    index += 1
            
        self.rpm1 = self.transmitted[0]
        self.rpm2 = self.transmitted[1]
        self.angle1 = self.transmitted[2]
        self.angle2 = self.transmitted[3]
    
    def print_data(self):
        print("rpm1 : {0} rpm2 : {1} angle1 : {2} angle2 : {3}".format(self.rpm1, self.rpm2, self.angle1, self.angle2))
        
def main():
    print('desktop ready')
    
    data = Data()
    while (True):
        ch5 = ser5.read().decode()
        if (ch5 == '*'): # if read char is *, send sensor data
            # send data
            element = 100.124
            strcmd = '*' + '100.001' + ',' + '100.002' + ',' + '100.03' + ',' + '0.4' + ',' + '0.5' + ',' + '100.006' + ',' + '100.007' + ',' + '100.008' + ',' + '100.009' + '\r' + '\n'
            print('send data = ' , strcmd)
            ser5.write(strcmd.encode())
            
            # receive rpm or angle
            ch = ser6.read().decode()
            recv = ''
            while (ch != '\n'):
                recv = recv + ch
                ch = ser6.read().decode()
            
            splited_str = recv.split(',')
            data.str_to_float(splited_str)
            data.print_data()


main()