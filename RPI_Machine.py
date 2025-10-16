#!/usr/bin/env python3

from gpiozero import LED, MotionSensor
import time
import socket

target_host = "192.168.1.105"
target_port = 6769

def connect_to_target():
    global client
    print(f"Attempting to establish connection with {target_host}:{target_port}")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    print("Connection successful.")
connect_to_target()

led_pin = 18 # define led and buzzer pin
sensor_pin = 17 # define sensor pin
led = LED(led_pin)     
sensor = MotionSensor(sensor_pin)

sensor.wait_for_no_motion()

def loop():
    # Variables to hold the current and last states
    currentstate = False
    previousstate = False
    while True:
        # Make sure we are connected to target
        try:
            client.getpeername()
        except socket.error:
            print("Connection check failed, attempting reconnection.")
            led.on()
            connect_to_target()
        except Exception as e:
            print(f"An unknown error occured in the connection: {e}")
            led.on()
        # Read sensor state
        currentstate = sensor.motion_detected
        # If the sensor is triggered
        if currentstate == True and previousstate == False:
            led.on()
            try:
                client.send(bytes("motion", "utf-8"))
                print("Sent data to target.")
            except:
                print("Failed to send data to target.")
                print("Retrying connection...")
                connect_to_target()
            print("Motion detected!")
            # Record previous state
            previousstate = True
        # If the sensor has returned to ready state
        elif currentstate == False and previousstate == True:
            led.off()
            print("No motion.")
            previousstate = False
        # Wait for 10 milliseconds
        time.sleep(0.01)

def destroy():
    client.close()
    led.close() 
    sensor.close()
    response = client.recv(4096)
    print(response.decode())

if __name__ == '__main__': # Program entrance
    print("Program started.")
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program
        destroy()
        print("Program exiting...")