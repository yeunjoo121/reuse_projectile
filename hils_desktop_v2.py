from cmath import nan
import time
import serial
import random

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

def main():
    data = [float(0), float(0), float(0), float(0)]
    index = 0
    first = 0
    maxlen = 80
    length = 0
    print('desktop ready')
    
    while (True):
        index = 0
        ch5 = ser5.read().decode()
        if (ch5 == '*'): # if read char is *, send sensor data
            # send data
            element = float(random.random())
            if (first == 0):
                first = 1
                strcmd = '*' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + (str)(element) + '\r\n'
            else:
                strcmd = '*' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + ',' + (str)(element) + '\r\n'
            print('send data = ' , strcmd)
            ser5.write(strcmd.encode())
            # receive rpm or angle
            ch = ser6.read().decode()
            recv = ''
            while (ch != '\n'): # 여기서 receive 예외처리 추가
                if (ch == ','):
                    if (index >= 4): # index가 4보다 크면 에러처리.
                        recv = ''
                        while (ch != '\n'):
                            ch = ser6.read().decode()
                        continue
                    data[index] = float(recv)
                    index += 1
                    recv = ''
                else:
                    recv += ch
                ch = ser6.read().decode()
                length += 1
                if (length > maxlen):
                    # 오류 시 nan으로 처리. 오류가 나도 new line이 올 때까지 한 세트를 읽어들여 다음 세트에 지장이 가지 않도록 함
                    length = 0
                    recv = nan
                    while (ch != '\n'):
                        ch = ser6.read().decode()
            data[index] = float(recv)
            print('rpm1 : ' , data[0])
            print('rpm2: ' , data[1])
            print('angle1: ' , data[2])
            print('angle2 : ' , data[3])
            
            print(type(data[0]))
            print(type(data[1]))
            print(type(data[2]))
            print(type(data[3]))

main()