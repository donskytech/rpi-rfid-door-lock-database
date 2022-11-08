import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import signal
import sys
import requests
import time

API_URL = 'http://192.168.100.22:5000/api/students'

RED_LED_PIN = 11
GREEN_LED_PIN = 13
BUZZER_PIN = 37
RELAY_PIN = 31

is_reading = True
current_rfid = None
reader = None

# Capture SIGINT for cleanup
def end_read(signal, frame):
    global is_reading
    print('Cleaning up GPIO before exiting...')
    GPIO.cleanup()
    is_reading = False
    sys.exit()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)


def get_rfid_info(rfid_badge_number):
    query_params = {
        "rfId": rfid_badge_number.strip()
    }
    response = requests.get(API_URL, params=query_params)

    return response.json()


def setup():
    global reader
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)

    reader = SimpleMFRC522()


def clear_outputs():
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)


def show_invalid_rfid():
    clear_outputs()
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1.0)
    clear_outputs()


def show_valid_rfid():
    clear_outputs()
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    open_lock()
    clear_outputs()


def open_lock():
    print("Opening door lock...")
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(RELAY_PIN, GPIO.LOW)


def main():
    global reader, current_rfid
    setup()

    print("Please scan your RFID(s)...")
    while is_reading:
        print("Here in looping...")
        _, text = reader.read()
        print("Blocking operation...")
        print(f"Text :: {text}")
        if text == current_rfid:
            time.sleep(1)
            current_rfid = None
        else:
            current_rfid = text
            response = get_rfid_info(text)
            print(f"Response :: {response}")
            if response:
                show_valid_rfid()
            else:
                show_invalid_rfid()


if __name__ == '__main__':
    main()
