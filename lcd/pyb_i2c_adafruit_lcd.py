"""Implements a HD44780 character LCD connected via MCP23008 on I2C.
   This was tested with: https://www.adafruit.com/product/292"""

from lcd_api import LcdApi
from pyb import I2C
from pyb import delay

# The MCP23008 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x20

# MCP23008 Registers

IODIR   = 0x00
IPOL    = 0x01
GPINTEN = 0x02
DEFVAL  = 0x03
INTCON  = 0x04
IOCON   = 0x05
GPPU    = 0x06
INTF    = 0x07
INTCAP  = 0x08
GPIO    = 0x09
OLAT    = 0x0A

# Defines shifts or masks for the various LCD line attached to the MCP23008

# GP0 - NC
# GP1 - RS
# GP2 - E
# GP3 - DB4
# GP4 - DB5
# GP5 - DB6
# GP6 - DB7
# GP7 - LITE

MASK_RS = 0x02
MASK_E = 0x04
SHIFT_DATA = 3
SHIFT_BACKLIGHT = 7


class I2cLcd(LcdApi):
    """Implements a HD44780 character LCD connected via MCP23008 on I2C."""

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr

        # Send IODIR address, set IODIR to all inputs, init all other registers 0
        self.i2c.send(b'\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00', self.i2c_addr)

        # Set pins GP1 through GP7 to output, leave GP0 as input
        self.i2c.mem_write(0x01, self.i2c_addr, IODIR)

        # Send reset 3 times
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        delay(5)    # need to delay at least 4.1 msec
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        delay(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        delay(1)
        # Put LCD into 4 bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        delay(1)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        """Writes an initialization nibble to the LCD.

        This particular function is only used during initialization.
        """
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        self.i2c.mem_write(byte | MASK_E, self.i2c_addr, GPIO)
        self.i2c.mem_write(byte, self.i2c_addr, GPIO)

    def hal_backlight_on(self):
        """Allows the hal layer to turn the backlight on."""
        self.i2c.mem_write(1 << SHIFT_BACKLIGHT, self.i2c_addr, GPIO)

    def hal_backlight_off(self):
        """Allows the hal layer to turn the backlight off."""
        self.i2c.mem_write(0, self.i2c_addr, GPIO)

    def hal_write_command(self, cmd):
        """Writes a command to the LCD.

        Data is latched on the falling edge of E.
        """
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.mem_write(byte | MASK_E, self.i2c_addr, GPIO)
        self.i2c.mem_write(byte, self.i2c_addr, GPIO)
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                ((cmd & 0x0f) << SHIFT_DATA))
        self.i2c.mem_write(byte | MASK_E, self.i2c_addr, GPIO)
        self.i2c.mem_write(byte, self.i2c_addr, GPIO)
        if cmd <= 3:
            # The home and clear commands require a worst
            # case delay of 4.1 msec
            delay(5)

    def hal_write_data(self, data):
        """Write data to the LCD."""
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                (((data >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.mem_write(byte | MASK_E, self.i2c_addr, GPIO)
        self.i2c.mem_write(byte, self.i2c_addr, GPIO)
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                ((data & 0x0f) << SHIFT_DATA))
        self.i2c.mem_write(byte | MASK_E, self.i2c_addr, GPIO)
        self.i2c.mem_write(byte, self.i2c_addr, GPIO)
