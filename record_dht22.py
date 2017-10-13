#!/usr/bin/python

import time
import logging
import urllib.request
import RPi.GPIO as GPIO
import Adafruit_DHT
from Display import Display

DHT22_DATA_PIN = 20
API_KEY = "M0859271I8O5JBB9"
BASE_URL = "https://api.thingspeak.com/update"
UPDATE_INTERVAL = 120

# View at:
# https://thingspeak.com/channels/346025/private_show

def update_multiple_fields(fields):
    try:
        logging.info('Sending update...')

        fields_url_part = '&'.join(['{}={}'.format(f,d) for f,d in fields.items()])
        url = "{}?api_key={}&{}".format(BASE_URL, API_KEY, fields_url_part)
        response = urllib.request.urlopen(url, timeout=10.0)

        logging.info('Sent update ({})'.format(response.status))

    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s', datefmt='%d/%m/%y %H:%M')
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    logging.info('Started')
    d = Display()
    try:
        while True:
            logging.info('Started Reading from DHT...')

            humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT22_DATA_PIN)
            if humidity is None or temp is None:
                logging.error('humidity/temp received are incorrect ({}.{})'.format(humidity,temp))
                continue

            temp, humidity = round(temp, 2), round(humidity, 2)
            text = "T/H: {:.1f}c {:.1f}%".format(temp, humidity)

            logging.info(text)
            d.write_line(text, 0)

            update_multiple_fields({1 : temp, 2: humidity})
            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt')

    finally:
        d.clear()
        GPIO.cleanup()
