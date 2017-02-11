"""Implements a HD44780 character LCD connected via PCF8574 on I2C."""

from i2c_lcd import I2cLcd
import time

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

def test_main():
    """Test function for verifying basic functionality."""
    lcd = I2cLcd(1, DEFAULT_I2C_ADDR, 2, 16)
    lcd.putstr("It Works!\nSecond Line")
    time.sleep(3)
    lcd.clear()
    count = 0
    while True:
        lcd.move_to(0, 0)
        lcd.putstr(time.strftime('%b %d %Y\n%H:%M:%S', time.localtime()))
        time.sleep(1)
        count += 1
        if count % 10 == 3:
            print "Turning backlight off"
            lcd.backlight_off()
        if count % 10 == 4:
            print "Turning backlight on"
            lcd.backlight_on()
        if count % 10 == 5:
            print "Turning display off"
            lcd.display_off()
        if count % 10 == 6:
            print "Turning display on"
            lcd.display_on()
        if count % 10 == 7:
            print "Turning display & backlight off"
            lcd.backlight_off()
            lcd.display_off()
        if count % 10 == 8:
            print "Turning display & backlight on"
            lcd.backlight_on()
            lcd.display_on()

if __name__ == "__main__":
    test_main()
