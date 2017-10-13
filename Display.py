#!/usr/bin/python

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

import RPi.GPIO as GPIO
import time

LCD_RS = 16
LCD_E  = 12
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

LINES = {
    0: LCD_LINE_1,
    1: LCD_LINE_2,
}

class Display(object):
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
        GPIO.setup(LCD_E, GPIO.OUT)  # E
        GPIO.setup(LCD_RS, GPIO.OUT) # RS
        GPIO.setup(LCD_D4, GPIO.OUT) # DB4
        GPIO.setup(LCD_D5, GPIO.OUT) # DB5
        GPIO.setup(LCD_D6, GPIO.OUT) # DB6
        GPIO.setup(LCD_D7, GPIO.OUT) # DB7

        self._init_display()

    def _init_display(self):
        # Initialise display
        self._write_cmd(0x33) # 110011 Initialise
        self._write_cmd(0x32) # 110010 Initialise
        self._write_cmd(0x06) # 000110 Cursor move direction
        self._write_cmd(0x0C) # 001100 Display On,Cursor Off, Blink Off
        self._write_cmd(0x28) # 101000 Data length, number of lines, font size
        self._write_cmd(0x01) # 000001 Clear display
        time.sleep(E_DELAY)

    def _write_char(self, char):
        self._write_byte(char, LCD_CHR)

    def _write_cmd(self, cmd):
        self._write_byte(cmd, LCD_CMD)

    def _write_byte(self, data, mode=False):
        # Send byte to data pins
        # data = data
        # mode = True  for character
        #        False for command

        GPIO.output(LCD_RS, mode)  # RS

        # High data
        GPIO.output(LCD_D4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if data & 0x10:
            GPIO.output(LCD_D4, True)
        if data & 0x20:
            GPIO.output(LCD_D5, True)
        if data & 0x40:
            GPIO.output(LCD_D6, True)
        if data & 0x80:
            GPIO.output(LCD_D7, True)

        # Toggle 'Enable' pin
        self._toggle_enable()

        # Low data
        GPIO.output(LCD_D4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if data & 0x01:
            GPIO.output(LCD_D4, True)
        if data & 0x02:
            GPIO.output(LCD_D5, True)
        if data & 0x04:
            GPIO.output(LCD_D6, True)
        if data & 0x08:
            GPIO.output(LCD_D7, True)

        # Toggle 'Enable' pin
        self._toggle_enable()

    def _toggle_enable(self):
        # Toggle enable
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, True)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, False)
        time.sleep(E_DELAY)

    def write_line(self, message, line = 0):
        # Send string to display
        message = message.ljust(LCD_WIDTH, " ")

        self._write_cmd(LINES[line])

        for i in range(LCD_WIDTH):
            self._write_char(ord(message[i]))

    def clear(self):
        self._write_cmd(0x01)

