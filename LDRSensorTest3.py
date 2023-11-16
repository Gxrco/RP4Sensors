import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
pin_to_sensor = 7  # GPIO pin number
GPIO.setup(pin_to_sensor, GPIO.IN)

try:
    light_on = False
    start_time = None

    while True:
        sensor_state = GPIO.input(pin_to_sensor)

        # Detect when the sensor starts receiving light
        if sensor_state == GPIO.LOW and not light_on:
            light_on = True
            start_time = time.time()
            print("Sensor is receiving light")

        # Detect when the sensor stops receiving light
        elif sensor_state == GPIO.HIGH and light_on:
            light_on = False
            if start_time:
                duration = time.time() - start_time
                print(f"Light was on for {duration} seconds")
            start_time = None

        time.sleep(0.01)  # Sleep time

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
