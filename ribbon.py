#!/usr/bin/python

import time
from display import Display

LCD_DISPLAY_SIZE = 16
INTERVAL = 0.3

def ribbon(display, message, line=0, size=LCD_DISPLAY_SIZE):
    if len(message) < size:
        display.write_line(message, line)
        return

    buf = message + '  ' + message
    for i in range(len(message) + 2):
        time.sleep(INTERVAL)
        display.write_line(buf[i:i+size], line)

if __name__ == '__main__':
    ribbon(Display(), "this is my very very long message")