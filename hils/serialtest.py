import threading
import time
import serial

DEV_PLATFORM = 'DESKTOP'

if DEV_PLATFORM == 'DESKTOP':
    port = 'COM5'
else:
    port = '/dev/ttyS0'
baud = 115200

ser = serial.Serial(
    port = port,
    baudrate = baud,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 5
    )

line = ''
alive = True
endcommand = False

# 스레드

def readthread(ser):
    global line
    global endcommand
    
    print('readthread init')
    
    while alive:
        try:
            for c in ser.read():
                line += (chr(c))#아스키로 변환하는 함수
                if line.startswith('['):#[로 시작하는지
                    if line.endswith(']'):#]로 끝나는지
                        print('receive data=' + line)
                        if line == '[end]':
                            endcommand = True
                            print('end command\n')
                        # line reset
                        line = ''
                        ser.write('ok'.encode())
                else:
                    line = ''
        except Exception as e:
            print('read exception')
            
    print('thread exit')
    
    ser.close()
    
def main():
    global endcommand
    
    # 시리얼 스레드 생성
    
    thread = threading.Thread(target=readthread, args=(ser,))
    thread.daemon = True
    thread.start()
    
    if DEV_PLATFORM == 'DESKTOP':
        for count in range(0, 10):
            strcmd = '[test' + str(count) + ']'
            print('send data=' + strcmd)
            strencoding = strcmd.encode()
            ser.write(strencoding)
            time.sleep(1)
            
        strcmd = '[end]'
        ser.write(strcmd.encode())
        print('send data=' + strcmd)
        
    else:
        while True:
            time.sleep(1)
            if endcommand is True:
                break
            
    print('main exit')
    alive = False
    exit()
    
main()