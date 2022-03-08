import RPi.GPIO as GPIO
import time
import serial

GPIO.setwarnings(False)

# GPIO.setmode(GPIO.BCM) # 핀/포트 번호를 BCM모드로 참조
# 
# GPIO.setup(15, GPIO.IN) # RX is Data Input
# GPIO.setup(14, GPIO.OUT) # TX is Data Output
print(time.time())
EBIMU = serial.Serial('/dev/ttyUSB0',115200) # baudrate = 115200 = <sb5>

EBIMU.flushInput() # flushInout은 캐시에 받은 모든 데이터 폐기
print(time.time())
EBIMU.write(b'<lf>') # b는 binary, <lf>는 초기값 load
print(time.time())
EBIMU.write(b'<sor0>') # <sor0>는 polling mode (set output rate)
print(time.time())
time.sleep(0.6)
print(time.time())

EBIMU.flushInput()
EBIMU.write(b'*')
print(EBIMU.readline())




"""
i = 0
while (1):
    print(i, EBIMU.read(), flush = True)
    i += 1"""
"""
EBIMU.flushInput() # flushInout은 캐시에 받은 모든 데이터 폐기
EBIMU.write(b'<sor0>') # <sor0>는 polling mode (set output rate)
time.sleep(0.1)

print(EBIMU.read())

EBIMU.flushInput() # flushInout은 캐시에 받은 모든 데이터 폐기
EBIMU.write(b'<sof1>') # <sof1>는 Euler Angles 출력
time.sleep(0.1)

print(EBIMU.read())

EBIMU.flushInput() # flushInout은 캐시에 받은 모든 데이터 폐기
EBIMU.write(b'<sog1>') # <sog1>은 자이로(각속도) 데이터 출력
time.sleep(1)

print(EBIMU.read())

EBIMU.flushInput() # flushInout은 캐시에 받은 모든 데이터 폐기
EBIMU.write(b'<soa1>') # <soa1>는 가속도 데이터 출력 
time.sleep(1)

print(EBIMU.read())

time.sleep(.3)
# EBIMU.flushInput() # flushInout은 캐시에 받은 모든 데이터 폐기

time.time() # unix 1970.01.01 이후로부터 지금까지의 걸린 시간을 초로 return
Hz = 100
dt = 1/Hz
time_old = 0

# print("zzz")
# EBIMU.write(b'*') # 안해주면 데이터 못읽음
while True:
    print(EBIMU.read())
EBIMU.flushInput() # flushInout은 캐시에 받은 모든 데이터 폐기
while True:
    a=EBIMU.read()
    print(a)
    """
"""
while True:
    while time_old + dt > time.time(): # 이 조건이 없으면 time_now - time_old 가 0에 수렴한다 
        time.sleep(dt*0.01)
    time_now = time.time()
    freq = 1/(time_now - time_old)
    time_old = time_now
    
    print(freq)

    # sensor data
    for i in range(1):
        print("zzz")
        EBIMU.write(b'*') # 안해주면 데이터 못읽음
        s = EBIMU.read(1) # 데이터 하나씩만 읽음
        print(s)
        if s == b'*':
            data = b''
            print(freq)
            while s != b'\n':
                s = EBIMU.read(1)
                data = data + s
            data = data[0:len(data)-2]
            print(data)
            transmitted_string = data.decode('utf-8') # 바이트 객체로 정의된 문자열을 유니코드 문자열로 변환 
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
            print("Gyro_X : {0} Gyro_Y : {1} Gyro_ Z : {2}".format(Gyro_X, Gyro_Y, Gyro_Z))
            print("X_acc : {0} Y_acc : {1} Z_acc : {2}".format(X_acc, Y_acc, Z_acc))
            print("\n")
"""
EBIMU.close()