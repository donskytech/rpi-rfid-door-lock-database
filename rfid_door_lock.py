import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import signal
import sys
import requests
import time

# IMPORTANT - CHANGE THIS!!!!!
# Define the IP Address endpoint of your REST API Endpoints
API_URL = 'http://192.168.100.22:5000/api/students'

# Define PIN assignments
RED_LED_PIN = 11
GREEN_LED_PIN = 13
BUZZER_PIN = 37
RELAY_PIN = 31

# Define variables for use in the program
is_reading = True
current_rfid = None
# Define our RFID Reader
reader = None

''' Cleanup function when the program is terminated '''
def end_read(signal, frame):
    global is_reading
    print('Cleaning up GPIO before exiting...')
    GPIO.cleanup()
    is_reading = False
    sys.exit()


''' Hook function when the program is terminated '''
signal.signal(signal.SIGINT, end_read)

''' Function to call the REST API function and validate the RFID Badge '''
def get_rfid_info(rfid_badge_number):
    query_params = {
        "rfId": rfid_badge_number.strip()
    }
    response = requests.get(API_URL, params=query_params)

    return response.json()


''' Initialize our pins and rfid reader '''
def setup():
    global reader
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)

    reader = SimpleMFRC522()


''' Clear the LED and Buzzer '''
def clear_outputs():
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)


'''If RFID is invalid then the Red LED and Buzzer is turned on'''
def show_invalid_rfid():
    clear_outputs()
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1.0)
    clear_outputs()


'''If RFID is valid then the Green LED and Solenoid Lock is turned on'''
def show_valid_rfid():
    clear_outputs()
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    open_lock()
    clear_outputs()


'''Unlock the door lock and close after 3 seconds'''
def open_lock():
    print("Opening door lock...")
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(RELAY_PIN, GPIO.LOW)


'''Our main entry function that calls the setup() method and periodically scans for RFID'''
def main():
    global reader, current_rfid
    setup()

    print("Please scan your RFID(s)...")
    while is_reading:
        _, rfid_badge_number = reader.read()
        strip_rfid_badge_number = rfid_badge_number.replace('\x00', '')

        if len(strip_rfid_badge_number.strip()) :
            if strip_rfid_badge_number == current_rfid:
                time.sleep(1)
                current_rfid=None
            else:
                current_rfid=strip_rfid_badge_number
                response=get_rfid_info(strip_rfid_badge_number)
                print(f"Response :: {response}")
                if response:
                    show_valid_rfid()
                    print("Access Granted")
                else:
                    show_invalid_rfid()
                    print("Access Denied")
        else:
            print("Invalid RFID Tag!")
            show_invalid_rfid()


# Main entry Point
if __name__ == '__main__':
    main()
