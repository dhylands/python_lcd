"""Implements a SeeedStudio Grove RGB LCD JHD1313M1 HD44780 compatible character LCD connected on I2C."""

from pyb import I2C, delay, millis
from pyb_i2c_grove_rgb_lcd import I2cLcd

import time
from urandom import getrandbits

# No jumper selectable address
DEFAULT_LCD_I2C_ADDR = 0x3e
# Software configurable address
DEFAULT_RGB_I2C_ADDR = 0x62

def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    i2c = I2C(1, I2C.MASTER)
    lcd = I2cLcd(i2c, DEFAULT_LCD_I2C_ADDR, 2, 16, DEFAULT_RGB_I2C_ADDR)
    lcd.putstr("It Works!\nSecond Line")
    lcd.backlight_rgb(255,255,255)
    lcd.blink_cursor_on()
    time.sleep_ms(1000)

    lcd.clear()
    lcd.putstr("Seeed Grove LCD RGB Backlight")
    time.sleep_ms(1000)

    # 16 columns, 2 rows
    lcd.clear()
    lcd.putstr("1234567890123456abcdefghijklmnop")
    time.sleep_ms(1000)

    lcd.hide_cursor();
    lcd.clear()
    lcd.putstr("Red")
    lcd.backlight_rgb(255,0,0)
    time.sleep_ms(1000)

    lcd.clear()
    lcd.putstr("Green")
    lcd.backlight_rgb(0,255,0)
    time.sleep_ms(1000)

    lcd.clear()
    lcd.putstr("Blue")
    lcd.backlight_rgb(0,0,255)
    time.sleep_ms(1000)

    # invert background colour
    lcd.clear()
    lcd.putstr("Blue")
    time.sleep_ms(1000)
    lcd.backlight_invert_on()
    lcd.putstr(" Inverted")
    time.sleep_ms(1000)
    lcd.clear()
    lcd.putstr("Blue")
    lcd.backlight_invert_off()
    time.sleep_ms(1000)

    # pwm blinking
    lcd.clear()
    lcd.putstr("Blinking PWM\nDuty=127 Freq=1")
    lcd.backlight_rgb(255,0,0)
    lcd.backlight_blink(127,1)
    time.sleep_ms(2000)
    lcd.backlight_normal()

    lcd.clear()
    lcd.putstr("Blinking PWM\nDuty=100 Freq=10")
    lcd.backlight_rgb(255,255,0)
    lcd.backlight_blink(100,10)
    time.sleep_ms(2000)
    lcd.backlight_normal()

    lcd.clear()
    lcd.putstr("Blinking PWM\nDuty=10 Freq=20")
    lcd.backlight_rgb(0,255,255)
    lcd.backlight_blink(10,20)
    time.sleep_ms(5000)
    lcd.backlight_normal()

    # pwm global brightness
    lcd.clear()
    lcd.putstr("Brightness 255")
    lcd.backlight_brightness(255)
    time.sleep_ms(1000)
    lcd.clear()
    lcd.putstr("Brightness 127")
    lcd.backlight_brightness(127)
    time.sleep_ms(1000)
    lcd.clear()
    lcd.putstr("Brightness 63")
    lcd.backlight_brightness(63)
    time.sleep_ms(1000)
    lcd.clear()
    lcd.putstr("Brightness 1")
    lcd.backlight_brightness(1)
    time.sleep_ms(1000)
    lcd.clear()
    lcd.putstr("Brightness 0")
    lcd.backlight_brightness(0)
    time.sleep_ms(1000)

    # take the rgb driver oscillator offline
    lcd.clear()
    lcd.backlight_normal()
    lcd.backlight_brightness(255)
    lcd.backlight_rgb(255,0,0)

    # low power mode
    lcd.backlight_sleep()
    lcd.putstr("low power mode\n")
    time.sleep_ms(2000)

    # cant change background colour while oscillator is offline
    lcd.backlight_rgb(0,255,255)
    lcd.putstr("cant change bg")
    time.sleep_ms(2000)

    # full power mode
    lcd.clear()
    lcd.putstr("full power mode\n")
    lcd.backlight_wake()
    # pending change applied
    lcd.putstr("bg now changed")
    time.sleep_ms(2000)

    # rainbow
    lcd.clear()
    lcd.putstr("Rainbow")
    for i in range(2):
        rainbow(lcd, 10)
    time.sleep_ms(1000)

    # random
    lcd.clear()
    lcd.putstr("Random")
    randomColors(lcd, 30, 100)


# Helper for converting 0-255 offset to a colour tuple
def wheel(offset):
    # The colours are a transition r - g - b - back to r
    offset = 255 - offset
    if offset < 85:
        return (255 - offset * 3, 0, offset * 3)
    if offset < 170:
        offset -= 85
        return (0, offset * 3, 255 - offset * 3)
    offset -= 170
    return (offset * 3, 255 - offset * 3, 0)

# Helper for setting a colour tuple
def hue(lcd, n):
    r,g,b = wheel(n & 255)
    lcd.backlight_rgb(r,g,b)

# cycle through all colours of the rainbow
def rainbow(lcd, sleep):
    for n in range(256):
        hue(lcd, n)
        time.sleep_ms(sleep)

# show n random colours
def randomColors(lcd, count, sleep):
    for r in range(count):
        r,g,b = (getrandbits(8), getrandbits(8), getrandbits(8))
        lcd.backlight_rgb(r,g,b)
        time.sleep_ms(sleep)

#if __name__ == "__main__":
test_main()
