"""Implements a character based lcd connected via PCF8574 on i2c."""

from pyb import Pin
from pyb import delay, millis
from pyb_gpio_lcd import GpioLcd

def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    lcd = GpioLcd(rs_pin=Pin.board.Y12,
                  enable_pin=Pin.board.Y11,
                  d4_pin=Pin.board.Y5,
                  d5_pin=Pin.board.Y6,
                  d6_pin=Pin.board.Y7,
                  d7_pin=Pin.board.Y8,
                  num_lines=4, num_columns=20)
    lcd.putstr("It Works!\nSecond Line\nThird Line\nFourth Line")
    delay(3000)
    lcd.clear()
    count = 0
    while True:
        lcd.move_to(0, 0)
        lcd.putstr("%7d" % (millis() // 1000))
        delay(1000)
        count += 1

