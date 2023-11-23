# Import necessary libraries
from mpu6050 import mpu6050
import RPi.GPIO as GPIO
import time
import csv

# Run the LDR sensor check in a separate thread
import threading

# Configure the GPIO to use the physical pin numbering
GPIO.setmode(GPIO.BOARD)

# Define the GPIO pin number connected to the LDR sensor
pin_to_sensor = 7
GPIO.setup(pin_to_sensor, GPIO.IN) # Set the pin as an input

# Initialize the MPU6050 accelerometer and gyroscope sensor
mpu = mpu6050(0x68)

# Declare a global variable to track the light state as detected by the LDR sensor
global lightFlag
lightFlag = False


# Define a function to monitor the LDR sensor
def ldrSensor():
    global lightFlag  # Use the global variable within this function
    try:
        light_on = False # Flag to track if the sensor is currently detecting light
        start_time = None # Variable to store the time when light detection starts

        while True:
            sensor_state = GPIO.input(pin_to_sensor) # Read the state of the LDR sensor

            # Detect when the sensor starts receiving light
            if sensor_state == GPIO.LOW and not light_on:
                light_on = True # Update the flag to indicate light is being detected
                start_time = time.time() # Record the start time
                lightFlag = True # Set the global flag to True
                print("Sensor is receiving light")

            # Detect when the sensor stops receiving light
            elif sensor_state == GPIO.HIGH and light_on:
                light_on = False # Update the flag to indicate light is no longer detected
                lightFlag = False # Set the global flag to False
                if start_time:
                    duration = time.time() - start_time # Calculate the duration of light exposure
                    print(f"Light was on for {duration} seconds")
                start_time = None # Reset the start time

            time.sleep(0.01) # Short delay to avoid overloading the CPU

    except KeyboardInterrupt:
        pass # Allow the program to be stopped manually

    finally:
        GPIO.cleanup() # Clean up GPIO resources


# Define a function to collect data from the MPU6050 sensor
def giroAcce():
    global lightFlag # Use the global variable within this function
    while True:
        if lightFlag:
            with open('mpu6050_data.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                
                # Write column headers to the CSV file
                writer.writerow(["Tiempo", "Temp", "Acc X", "Acc Y", "Acc Z", "Gyro X", "Gyro Y", "Gyro Z"])

                try:
                    for _ in range(10):  #Run the loop 10 times for testing
                        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                        try:
                            # Read temperature, accelerometer, and gyroscope data from MPU6050
                            temperature = mpu.get_temp()
                            accel_data = mpu.get_accel_data()
                            gyro_data = mpu.get_gyro_data()
                        except Exception as sensor_error:
                            print(f"Error reading from sensor: {sensor_error}")
                            continue

                        # Extract and store the individual accelerometer and gyroscope data
                        acc_x, acc_y, acc_z = accel_data['x'], accel_data['y'], accel_data['z']
                        gyro_x, gyro_y, gyro_z = gyro_data['x'], gyro_data['y'], gyro_data['z']

                        try:
                            # Write the sensor data to the CSV file
                            writer.writerow([current_time, temperature, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z])
                            file.flush() # Ensure data is written to the file immediately
                        except Exception as write_error:
                            print(f"Error writing to file: {write_error}")
                            break

                        print(f"Tiempo: {current_time}, Temp: {temperature}, Acc: ({acc_x}, {acc_y}, {acc_z}), Gyro: ({gyro_x}, {gyro_y}, {gyro_z})")
                        time.sleep(1)

                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
        else:
            # Print a message when the LDR sensor is not detecting light
            print("Please expose the LDR sensor to light to keep retrieving data from the giroscope and accelerometer.")
            time.sleep(1)  # Add some delay to avoid flooding the console

# Start the LDR sensor monitoring in a separate thread
ldr_thread = threading.Thread(target=ldrSensor)
ldr_thread.start()

# Run the MPU6050 data collection
giroAcce()
