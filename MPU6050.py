#!/usr/bin/env python

"""
  author: Ugurcan Dede
  date: 5/7/2020

  description: Simple MPU6050 Python Application Written Using I2C and SMBus
  project-url: https://github.com/ugurcandede/MPU6050-i2c

"""

from smbus2 import SMBus
import math
import time

SLAVE_ADDR = 0x68

PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C
WHO_AM_I = 0x75

GYRO_X = 0x43
GYRO_Y = 0x45
GYRO_Z = 0x47

ACCL_X = 0x3B
ACCL_Y = 0x3D
ACCL_Z = 0x3F

bus = SMBus(1)
bus.write_byte_data(SLAVE_ADDR, PWR_MGMT_1, 0)

def read_byte(addr):
    return bus.read_byte_data(SLAVE_ADDR,addr)

def read_word(addr):
    h = bus.read_byte_data(SLAVE_ADDR, addr)
    l = bus.read_byte_data(SLAVE_ADDR, addr+1)
    val = (h << 8) + l
    return val

def read_word_i2c(addr):
    val = read_word(addr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(x, y):
    return math.sqrt((x*x) + (y*y))

def get_x_rotat(x,y, z):
    rad = math.atan2(y, dist(x, z))
    return math.degrees(rad)

def get_y_rotat(x, y, z):
    rad = math.atan2(x, dist(y, z))
    return -math.degrees(rad)

def read_gyro():
    GYR_X = read_word_i2c(GYRO_X)
    GYR_Y = read_word_i2c(GYRO_Y)
    GYR_Z = read_word_i2c(GYRO_Z)

    print ("GYRO -> X:{:04.2f} Y:{:04.2f} Z:{:04.2f}".format((GYR_X/131), (GYR_Y/131), (GYR_Z/131)))

def read_acc():
    ACC_X = read_word_i2c(ACCL_X)
    ACC_Y = read_word_i2c(ACCL_Y)
    ACC_Z = read_word_i2c(ACCL_Z)

    CALC_ACC_X = ACC_X/16384.0
    CALC_ACC_Y = ACC_Y/16384.0
    CALC_ACC_Z = ACC_Z/16384.0

    print ("ACCL -> X:{:04.2f} Y:{:04.2f} Z:{:04.2f}".format(CALC_ACC_X, CALC_ACC_Y, CALC_ACC_Z))
    print("ROTATE -> X:{:04.2f} Y:{:04.2f}\n".format(get_x_rotat(CALC_ACC_X, CALC_ACC_Y, CALC_ACC_Z), get_y_rotat(CALC_ACC_X, CALC_ACC_Y, CALC_ACC_Z)))

while True:
    read_gyro()
    read_acc()
    time.sleep(1)
