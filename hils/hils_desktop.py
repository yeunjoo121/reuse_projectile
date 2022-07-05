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
    print('desktop ready')
    while (True):
        ch5 = ser5.read().decode()
        ch6 = ser6.read().decode()
        if (ch5 == '*'): # if read char is *, send sensor data
            # send data
            strcmd = '*0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0\r\n'
            print('send data = ' + strcmd)
            ser5.write(strcmd.encode())
        if (ch6 > 0): # if read byte is greater than 0 (return value is number of bytes to read)
            # receive rpm or angle
            recv = ''
            temp = ser6.read().decode()
            while (temp > 0):
                recv += temp
                temp = ser6.read().decode()
            recv = recv[0:len(recv) - 1]
            print('recv = ' + recv)


main()