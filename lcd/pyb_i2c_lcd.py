"""Implements a character based lcd connected via PCF8574 on i2c."""

from lcd import LcdApi
from pyb import I2C
from pyb import delay, millis

DEFAULT_I2C_ADDR = 0x27

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
        self.i2c.send(0, self.i2c_addr)
        delay(20)   # Allow LCD time to powerup
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


        This particular function is only used during intiialization.
        """
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        self.i2c.send(byte | MASK_E, self.i2c_addr)
        self.i2c.send(byte, self.i2c_addr, )

    def hal_backlight_on(self):
        """Allows the hal layer to turn the backlight on."""
        self.i2c.send(1 << SHIFT_BACKLIGHT, self.i2c_addr)

    def hal_backlight_off(self):
        """Allows the hal layer to turn the backlight off."""
        self.i2c.send(0, self.i2c_addr)

    def hal_write_command(self, cmd):
        """Writes a command to the LCD.

        Data is latched on the falling edge of E.
        """
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.send(byte | MASK_E, self.i2c_addr)
        self.i2c.send(byte, self.i2c_addr)
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                ((cmd & 0x0f) << SHIFT_DATA))
        self.i2c.send(byte | MASK_E, self.i2c_addr, )
        self.i2c.send(byte, self.i2c_addr)
        if cmd <= 3:
            # The home and clear commands require a worst
            # case delay of 4.1 msec
            delay(5)

    def hal_write_data(self, data):
        """Write data to the LCD."""
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                (((data >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.send(byte | MASK_E, self.i2c_addr)
        self.i2c.send(byte, self.i2c_addr)
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                ((data & 0x0f) << SHIFT_DATA))
        self.i2c.send(byte | MASK_E, self.i2c_addr)
        self.i2c.send(byte, self.i2c_addr)

def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    i2c = I2C(1, I2C.MASTER)
    lcd = I2cLcd(i2c, 0x27, 2, 16)
    lcd.putstr("It Works!\nSecond Line")
    delay(3000)
    lcd.clear()
    count = 0
    while True:
        lcd.move_to(0, 0)
        lcd.putstr("%7d" % (millis() // 1000))
        delay(1000)
        count += 1
        if count % 10 == 3:
            print("Turning backlight off")
            lcd.backlight_off()
        if count % 10 == 4:
            print("Turning backlight on")
            lcd.backlight_on()
        if count % 10 == 5:
            print("Turning display off")
            lcd.display_off()
        if count % 10 == 6:
            print("Turning display on")
            lcd.display_on()
        if count % 10 == 7:
            print("Turning display & backlight off")
            lcd.backlight_off()
            lcd.display_off()
        if count % 10 == 8:
            print("Turning display & backlight on")
            lcd.backlight_on()
            lcd.display_on()

#if __name__ == "__main__":
#test_main()

