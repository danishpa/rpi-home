#!/usr/bin/python

import sys
from display import Display

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) > 3 or len(argv) < 2:
        print('./write_lcd.py <first line> [second line]')

    first = argv[1]
    second = ''
    if len(argv) == 3:
        second = argv[2]

    d = Display()
    d.write_line(first, 0)
    d.write_line(second, 1)
