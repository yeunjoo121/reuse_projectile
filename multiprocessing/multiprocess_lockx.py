from multiprocessing import Process, Value, Array
import time
import os

def add_100(number):
    for i in range(100):
        time.sleep(0.01)
        number.value += 1

def min_100(number):
    for i in range(100):
        time.sleep(0.01)
        number.value -= 1

if __name__ == "__main__":

    shared_number = Value('i', 0)
    print("Number at beginning is", shared_number)

    p1 = Process(target=add_100, args=(shared_number,))
    p2 = Process(target=min_100, args=(shared_number,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print("number at end is", shared_number)