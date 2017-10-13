#!/usr/bin/python

import time
from display import Display

LCD_DISPLAY_SIZE = 16
INTERVAL = 0.15
SEPERATOR = '   '

def ribbon(display, message, line=0, size=LCD_DISPLAY_SIZE, separator=SEPERATOR):
    if len(message) < size:
        display.write_line(message, line)
        return

    buf = message + separator + message
    while True:
        for i in range(len(message) + len(separator)):
            time.sleep(INTERVAL)
            display.write_line(buf[i:i+size], line)

if __name__ == '__main__':
    d = Display()
    try:
        ribbon(d, "this is my very long test message")
    except KeyboardInterrupt:
        d.clear()
