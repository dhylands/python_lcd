"""Implements a character based lcd connected via PCF8574 on i2c."""

from lcd_api import LcdApi
from machine import I2C
import utime

DEFAULT_I2C_ADDR = 0x3f

# Defines shifts or masks for the various LCD line attached to the PCF8574

MASK_RS = 0x01
MASK_RW = 0x02
MASK_E = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4


class I2cLcd(LcdApi):
    """Implements a character based lcd connected via PCF8574 on i2c."""

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.write(self.i2c_addr, 0)
        utime.sleep_ms(20)  # Allow LCD time to powerup
        # Send reset 3 times
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(5)  # need to utime.sleep_ms at least 4.1 msec
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)
        # Put LCD into 4 bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        utime.sleep_ms(1)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def write(self, address, byte):
        self.i2c.writeto(address, bytes([byte]))

    def hal_write_init_nibble(self, nibble):
        """Writes an initialization nibble to the LCD.


        This particular function is only used during intiialization.
        """
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        self.write(self.i2c_addr, byte | MASK_E)
        self.write(self.i2c_addr, byte)

    def hal_backlight_on(self):
        """Allows the hal layer to turn the backlight on."""
        self.write(self.i2c_addr, 1 << SHIFT_BACKLIGHT)

    def hal_backlight_off(self):
        """Allows the hal layer to turn the backlight off."""
        self.write(self.i2c_addr, 0)

    def hal_write_command(self, cmd):
        """Writes a command to the LCD.

        Data is latched on the falling edge of E.
        """
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        self.write(self.i2c_addr, byte | MASK_E)
        self.write(self.i2c_addr, byte)
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                ((cmd & 0x0f) << SHIFT_DATA))
        self.write(self.i2c_addr, byte | MASK_E)
        self.write(self.i2c_addr, byte)
        if cmd <= 3:
            # The home and clear commands require a worst
            # case delay of 4.1 msec
            utime.sleep_ms(5)

    def hal_write_data(self, data):
        """Write data to the LCD."""
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                (((data >> 4) & 0x0f) << SHIFT_DATA))
        self.write(self.i2c_addr, byte | MASK_E)
        self.write(self.i2c_addr, byte)
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                ((data & 0x0f) << SHIFT_DATA))
        self.write(self.i2c_addr, byte | MASK_E)
        self.write(self.i2c_addr, byte)
