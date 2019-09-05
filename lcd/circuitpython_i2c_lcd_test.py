"""Implements a HD44780 character LCD connected via PCF8574 on I2C in CircuitPython.
   This was tested with the Adafruit Trinket M0
   https://www.adafruit.com/product/3500"""

import board
import busio
from time import sleep, monotonic
from circuitpython_i2c_lcd import I2cLcd

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    i2c = busio.I2C(board.SCL, board.SDA)

    # circuitpython seems to require locking the i2c bus
    while i2c.try_lock():
        pass

    # 2 lines, 16 characters per line
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

    # smiley faces as custom characters
    happy = bytearray([0x00,0x0A,0x00,0x04,0x00,0x11,0x0E,0x00])
    sad = bytearray([0x00,0x0A,0x00,0x04,0x00,0x0E,0x11,0x00])
    grin = bytearray([0x00,0x00,0x0A,0x00,0x1F,0x11,0x0E,0x00])
    shock = bytearray([0x0A,0x00,0x04,0x00,0x0E,0x11,0x11,0x0E])
    meh = bytearray([0x00,0x0A,0x00,0x04,0x00,0x1F,0x00,0x00])
    angry = bytearray([0x11,0x0A,0x11,0x04,0x00,0x0E,0x11,0x00])
    tongue = bytearray([0x00,0x0A,0x00,0x04,0x00,0x1F,0x05,0x02])
    lcd.custom_char(0, happy)
    lcd.custom_char(1, sad)
    lcd.custom_char(2, grin)
    lcd.custom_char(3, shock)
    lcd.custom_char(4, meh)
    lcd.custom_char(5, angry)
    lcd.custom_char(6, tongue)

    lcd.putstr("It works!\nSecond line")
    sleep(3)
    lcd.clear()
    lcd.putstr("Custom chars:\n")
    for i in range(7):
        lcd.putchar(" ")
        lcd.putchar(chr(i))
        sleep(1)

    sleep(3)
    lcd.clear()
    count = 0

    while True:
        lcd.move_to(0, 0)
        lcd.putstr("%7d" % monotonic())
        sleep(1)
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
        if count % 10 == 7:
            print("Turning display & backlight off")
            lcd.backlight_off()
            lcd.display_off()
        if count % 10 == 8:
            print("Turning display & backlight back on")
            lcd.backlight_on()
            lcd.display_on()

#if __name__ == "__main__":
test_main()