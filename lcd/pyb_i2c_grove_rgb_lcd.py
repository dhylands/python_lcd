"""Implements a SeeedStudio Grove RGB LCD JHD1313M1 HD44780 compatible character LCD connected on I2C."""

from lcd_api import LcdApi
from pyb import delay

# No jumper selectable address
DEFAULT_LCD_I2C_ADDR = 0x3e
# Software configurable address
DEFAULT_RGB_I2C_ADDR = 0x62

class I2cLcd(LcdApi):
    """Implements a HD44780 character LCD connected to I2C."""

    def __init__(self, i2c, i2c_addr, num_lines, num_columns, bl_i2c_addr):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.bl_i2c_addr = bl_i2c_addr
        # Put LCD into 4 bit mode
        self.hal_write_command(self.LCD_FUNCTION)
        delay(1)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)
        # init backlight
        self.i2c.mem_write(0, self.bl_i2c_addr, 0) # MODE1
        self.i2c.mem_write(0, self.bl_i2c_addr, 1) # MODE2

    def backlight_rgb(self, r, g, b):
        self.i2c.mem_write(170, self.bl_i2c_addr, 8) # LEDOUT
        self.i2c.mem_write(r, self.bl_i2c_addr, 4) # Red
        self.i2c.mem_write(g, self.bl_i2c_addr, 3) # Green
        self.i2c.mem_write(b, self.bl_i2c_addr, 2) # Blue

    def backlight_invert_on(self):
        self.i2c.mem_write(16, self.bl_i2c_addr, 1) # MODE2 bit4 INVRT 1=on

    def backlight_invert_off(self):
        self.i2c.mem_write(0, self.bl_i2c_addr, 1) # MODE2 bit4 INVRT 0=off

    def backlight_blink(self, duty, freq):
        self.i2c.mem_write(32, self.bl_i2c_addr, 1) # MODE2 bit5 DMBLNK 1=blinking
        self.i2c.mem_write(255, self.bl_i2c_addr, 8) # LEDOUT = PWMx + GRPPWM
        # blink
        self.i2c.mem_write(duty, self.bl_i2c_addr, 6) # GRPPWM = duty cycle
        self.i2c.mem_write(freq, self.bl_i2c_addr, 7) # GRPFREQ = blinking period (24hz - 10.73s)

    def backlight_brightness(self, duty):
        self.i2c.mem_write(0, self.bl_i2c_addr, 1) # MODE2 bit5 DMBLNK 0=dimming
        self.i2c.mem_write(255, self.bl_i2c_addr, 8) # LEDOUT = PWMx + GRPPWM
        # set brightness
        self.i2c.mem_write(duty, self.bl_i2c_addr, 6) # GRPPWM = global brightness

    def backlight_normal(self):
        self.i2c.mem_write(170, self.bl_i2c_addr, 8) # LEDOUT = PWMx

    def backlight_sleep(self):
        self.i2c.mem_write(16, self.bl_i2c_addr, 0) # MODE1 bit4 SLEEP 1=low power mode, oscillator off

    def backlight_wake(self):
        self.i2c.mem_write(0, self.bl_i2c_addr, 0) # MODE1 bit4 SLEEP 0=normal power mode

    def hal_backlight_on(self):
        """Allows the hal layer to turn the backlight on."""
        self.i2c.mem_write(85, self.bl_i2c_addr, 0x08)

    def hal_backlight_off(self):
        """Allows the hal layer to turn the backlight off."""
        self.i2c.mem_write(0, self.bl_i2c_addr, 0x08)

    def hal_write_command(self, cmd):
        """Writes a command to the LCD."""
        self.i2c.mem_write(cmd, self.i2c_addr, self.LCD_DDRAM)
        if cmd <= 3:
            # The home and clear commands require a worst
            # case delay of 4.1 msec
            delay(5)

    def hal_write_data(self, data):
        """Write data to the LCD."""
        self.i2c.mem_write(data, self.i2c_addr, self.LCD_CGRAM)
