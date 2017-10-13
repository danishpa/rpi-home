#!/usr/bin/python
import time
import uuid
import datetime
import timeago
import logging
import urllib.request
import RPi.GPIO as GPIO
import Adafruit_DHT
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from Display import Display

# View at:
# https://thingspeak.com/channels/346025/private_show

DHT22_DATA_PIN = 20
API_KEY = 'M0859271I8O5JBB9'
BASE_URL = 'https://api.thingspeak.com/update'
UPDATE_DISPLAY_INTERVAL = 1.0
QUERY_INTERVAL = 120
DEFAULT_DATA_DISPLAY = 'T/H: N/A'

TEMPRATURE_FIELD_INDEX = 1
HUMIDITY_FIELD_INDEX = 2

class Monitor(object):
    def __init__(self):
        self._display = Display()
        self._logger = self._make_logger()
        self._logger.debug('Initialized Logger')
        self._last_query = None
        self._display_data = ''

        self._logger.info('Initialized')
        update_display = LoopingCall(self._update_display_last_query)
        query = LoopingCall(self._query_sensors_and_notify)

        self._tasks = [update_display, query]

        update_display.start(UPDATE_DISPLAY_INTERVAL)
        query.start(QUERY_INTERVAL)

    def __del__(self):
        if self._display:
            self._display.clear()

        GPIO.cleanup()

    @staticmethod
    def _make_logger():
        logger = logging.getLogger('Monitor/{}'.format(str(uuid.uuid4())))
        logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(levelname)s\t- %(message)s', datefmt='%d/%m/%y %H:%M:%S')
        sh.setFormatter(formatter)

        logger.addHandler(sh)
        return logger

    def _notify_thingspeak(self, fields):
        self._logger.debug('Sending update...')

        fields_url_part = '&'.join(['{}={}'.format(f,d) for f,d in fields.items()])
        url = '{}?api_key={}&{}'.format(BASE_URL, API_KEY, fields_url_part)
        response = urllib.request.urlopen(url, timeout=10.0)

        self._logger.debug('Sent update ({})'.format(response.status))

    def _update_display_data(self):
        self._display.write_line(self._display_data, 0)

    def _update_display_last_query(self):
        if not self._last_query:
            return

        self._display.write_line(timeago.format(self._last_query), 1)

    def _read_dht22(self):
        self._logger.debug('Started reading from DHT22')
        humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT22_DATA_PIN)
        self._logger.debug('Read from DHT22')
        return humidity, temp

    def _query_sensors(self):
        sensors = {}

        humidity, temp = self._read_dht22()
        if humidity is not None:
            sensors['humidity'] = round(humidity, 2)

        if temp is not None:
            sensors['temprature'] = round(temp, 2)

        self._last_query = datetime.datetime.now()
        return sensors

    def _format_sensor_readings(self, sensor_readings):
        if sensor_readings['humidity'] is None or sensor_readings['temprature'] is None:
            self._logger.error('humidity/temp received are incorrect ({}.{})'.format(humidity,temp))
            return DEFAULT_DATA_DISPLAY
        text = 'T/H: {:.1f}c {:.1f}%'.format(sensor_readings['temprature'], sensor_readings['humidity'])
        return text

    def _query_sensors_and_notify(self):
        sensor_readings = self._query_sensors()
        text = self._format_sensor_readings(sensor_readings)
        self._logger.info(text)

        self._display.write_line(text, 0)
        self._notify_thingspeak({
            TEMPRATURE_FIELD_INDEX : sensor_readings['temprature'],
            HUMIDITY_FIELD_INDEX   : sensor_readings['humidity']
        })

    def run(self):
        reactor.run()

if __name__ == '__main__':
    m = Monitor()
    m.run()


