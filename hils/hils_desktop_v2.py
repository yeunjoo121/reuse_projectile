import time
import serial

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
    rpm1 = 0 #1
    rpm2 = 0 #2
    angle1 = 0 #3
    angle2 = 0 #4
    index = 0
    print('desktop ready')
    while (True):
        ch5 = ser5.read().decode()
        if (ch5 == '*'): # if read char is *, send sensor data
            # send data
            strcmd = '*0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0\r\n'
            print('send data = ' + strcmd)
            ser5.write(strcmd.encode())
            for i in range(4):
                # receive rpm or angle
                recv = ''
                ch = ser6.read().decode()
                if (ch == '['): # rpm, angle format => [1]40\n or [3]3\n
                    index = ser6.read().decode()
                    ch = ser6.read().decode()
                    if (ch == ']'):
                        ch = ser6.read().decode()
                        while (ch != '\n'):
                            recv += ch
                            ch = ser6.read().decode()
                print('recv = ' + recv)
                # 이제 rpm, angle값을 주어진 변수에 대입
                if (index == '1'):
                    rpm1 = recv
                    print('rpm1 : ' , rpm1)
                elif (index == '2'):
                    rpm2 = recv
                    print('rpm2: ' , rpm2)
                elif (index == '3'):
                    angle1 = recv
                    print('angle1: ' , angle1)
                elif (index == '4'):
                    angle2 = recv
                    print('angle2 : ' , angle2)        

main()