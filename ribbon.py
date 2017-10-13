#!/usr/bin/python
import time
from display import Display

LCD_DISPLAY_SIZE = 16
INTERVAL = 0.15
SEPERATOR = '   '

def make_ribbon_gen(display, message, line=0, separator=SEPERATOR):
    if len(message) < display.width():
        display.write_line(message, line)
        return

    buf = message + separator + message
    while True:
        for i in range(len(message) + len(separator)):
            display.write_line(buf[i:i+display.width()], line)
            yield

def ribbon(display, message, line=0, separator=SEPERATOR, interval=INTERVAL):
    for x in make_ribbon_gen(display, message, line, separator):
        time.sleep(interval)

if __name__ == '__main__':
    d = Display()
    try:
        ribbon(d, "this is my very long test message")

    except KeyboardInterrupt:
        d.clear()
