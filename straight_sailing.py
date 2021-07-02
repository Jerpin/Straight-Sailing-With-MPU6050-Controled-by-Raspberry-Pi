import smbus
from time import sleep
from gpiozero import Motor
import RPi.GPIO as GPIO
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
motor = Motor(15,14)
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
bus = smbus.SMBus(1) 
address = 0x68       
bus.write_byte_data(address, power_mgmt_1, 0)

servo = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo, GPIO.OUT)
p = GPIO.PWM(servo, 50) 
p.start(5.5)
angle=0
t = 0.3
i = 0
z = 0

while True:
    try:
        motor.forward()
        sleep(t)
        gyro_z = read_word_2c(0x47)+208.59
        z += gyro_z
        alpha_z = gyro_z / 131
        angle = angle + alpha_z * t
        print("angle: %.2f" % angle)
        if angle>0.3:
            signal_width = 7.5
            print("L")
        elif angle<-0.3:
            signal_width = 3.5
            print("R")
        else:
            signal_width = 5.5
            print("F")
        p.ChangeDutyCycle(signal_width)
        i = i+1
        print("-----------")
    except:
        print("ERROR")
        continue


