"""Implements a HD44780 character LCD connected via MCP23008 on I2C."""

from pyb import I2C, delay, millis
from pyb_i2c_adafruit_lcd import I2cLcd

# The MCP23008 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x20

def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    i2c = I2C(1, I2C.MASTER)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 4, 20)
    lcd.putstr("It Works!\nSecond Line\nThird Line\nFourth Line")
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
test_main()
