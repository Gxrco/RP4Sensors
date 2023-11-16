# Import necessary libraries
from mpu6050 import mpu6050  # Library to interact with MPU6050 sensor
import time  # Time library for delay purposes

# Initialize the MPU6050 sensor
mpu = mpu6050(0x68)  # 0x68 is the default I2C address for the MPU6050

# Infinite loop to continuously read data from the sensor
while True:
    # Reading and printing the temperature from the MPU6050
    print("Temp : "+str(mpu.get_temp()))
    print()

    # Reading accelerometer data
    accel_data = mpu.get_accel_data()  # Retrieves a dictionary with accelerometer data
    # Printing accelerometer data in X, Y, Z axes
    print("Acc X : "+str(accel_data['x']))
    print("Acc Y : "+str(accel_data['y']))
    print("Acc Z : "+str(accel_data['z']))
    print()

    # Reading gyroscope data
    gyro_data = mpu.get_gyro_data()  # Retrieves a dictionary with gyroscope data
    # Printing gyroscope data in X, Y, Z axes
    print("Gyro X : "+str(gyro_data['x']))
    print("Gyro Y : "+str(gyro_data['y']))
    print("Gyro Z : "+str(gyro_data['z']))
    print()

    # Separator for readability
    print("-------------------------------")

    # Delay of 1 second before the next read
    time.sleep(1)
