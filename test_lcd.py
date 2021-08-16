#!/usr/bin/env python3

# This file tests the LcdApi class

import unittest

from lcd import LcdApi

DDRAM_SIZE = 128

class LcdSim(LcdApi):
    """Implements an HD44780 character LCD emulator.

       The addressing modes are described here:
       http://web.alfredstate.edu/faculty/weimandn/lcd/lcd_addressing/lcd_addressing_index.html
    """

    def __init__(self, num_lines=2, num_columns=16):
        LcdApi.__init__(self, num_lines, num_columns)
        self.reset()
        self.num_lines = num_lines
        self.num_columns = num_columns

    def hal_backlight_on(self):
        """Allows the hal layer to turn the backlight on."""

    def hal_backlight_off(self):
        """Allows the hal layer to turn the backlight off."""

    def hal_write_command(self, cmd):
        """Writes a command to the LCD.

        Data is latched on the falling edge of E.
        """
        if cmd == LcdApi.LCD_CLR:
            self.reset()
        elif cmd == LcdApi.LCD_HOME:
            self.addr = 0
        elif cmd & LcdApi.LCD_DDRAM != 0:
            self.addr = cmd & 0x7f

    def hal_write_data(self, data):
        """Write data to the LCD."""
        self.ddram[self.addr & 0x7f] = data
        self.addr += 1

    def reset(self):
        """Resets the DDRAM."""
        self.ddram = [ord(' ')] * DDRAM_SIZE
        self.addr = 0

    def display_lines(self):
        """Returns the DDRAM as an array of display lines."""
        lines = []
        for i in range(self.num_lines):
            addr = self.addr_for_line(i)
            line = bytes(self.ddram[addr:addr+self.num_columns])
            lines.append(line)
        return lines

    def addr_for_line(self, line):
        """Calculates the DDRAM address for a particular line."""

        # From http://web.alfredstate.edu/faculty/weimandn/lcd/lcd_addressing/lcd_addressing_index.html
        #
        #   2 x 40: 0x00, 0x40
        #   4 x 20: 0x00, 0x40, 0x14, 0x54
        #   2 x 20: 0x00, 0x40
        #   2 x 16: 0x00, 0x40
        #   4 x 16: 0x00, 0x40, 0x10, 0x50

        addr = 0
        if line & 1 != 0:
            addr += 0x40
        if line & 2 != 0:
          addr += self.num_columns
        return addr

    def dump_lines(self):
      lines = self.display_lines()
      for i in range(self.num_lines):
          line = lines[i].decode('utf-8','ignore')
          print('Line {}: {:02x} >{}<'.format(i, self.addr_for_line(i), line))


class TestLcd(unittest.TestCase):

  def test_simple(self):
    lcd = LcdSim(4, 20)
    lcd.putstr('Line 1')
    self.assertEqual(lcd.display_lines(), [
      b'Line 1              ',
      b'                    ',
      b'                    ',
      b'                    '
    ])
    lcd.putstr(': more\n')
    lcd.putstr('Line 2')
    self.assertEqual(lcd.display_lines(), [
      b'Line 1: more        ',
      b'Line 2              ',
      b'                    ',
      b'                    '
    ])

  def test_full_line(self):
    lcd = LcdSim(4, 20)
    lcd.putstr('Line 1 - 01234567890')
    self.assertEqual(lcd.display_lines(), [
      b'Line 1 - 01234567890',
      b'                    ',
      b'                    ',
      b'                    '
    ])
    lcd.putstr('Line 2 - 01234567890')
    self.assertEqual(lcd.display_lines(), [
      b'Line 1 - 01234567890',
      b'Line 2 - 01234567890',
      b'                    ',
      b'                    '
    ])
    lcd.putstr('Line 3 - 01234567890')
    lcd.putstr('Line 4 - 01234567890')
    lcd.putstr('Line 5 - 01234567890')
    self.assertEqual(lcd.display_lines(), [
      b'Line 5 - 01234567890',
      b'Line 2 - 01234567890',
      b'Line 3 - 01234567890',
      b'Line 4 - 01234567890',
    ])

  def test_full_line2(self):
    lcd = LcdSim(4, 20)
    lcd.putstr('Line 1 - 01234567890\n')
    self.assertEqual(lcd.display_lines(), [
      b'Line 1 - 01234567890',
      b'                    ',
      b'                    ',
      b'                    '
    ])
    lcd.putstr('Line 2 - 01234567890\n')
    self.assertEqual(lcd.display_lines(), [
      b'Line 1 - 01234567890',
      b'Line 2 - 01234567890',
      b'                    ',
      b'                    '
    ])
    lcd.putstr('Line 3 - 01234567890\n')
    lcd.putstr('Line 4 - 01234567890\n')
    lcd.putstr('Line 5 - 01234567890\n')
    self.assertEqual(lcd.display_lines(), [
      b'Line 5 - 01234567890',
      b'Line 2 - 01234567890',
      b'Line 3 - 01234567890',
      b'Line 4 - 01234567890',
    ])

  def test_simple_4x16(self):
    lcd = LcdSim(4, 16)
    lcd.putstr('Line 1\n')
    lcd.putstr('Line 2\n')
    lcd.putstr('Line 3\n')
    lcd.putstr('Line 4\n')
    self.assertEqual(lcd.display_lines(), [
      b'Line 1          ',
      b'Line 2          ',
      b'Line 3          ',
      b'Line 4          ',
    ])


if __name__ == '__main__':
    unittest.main()
