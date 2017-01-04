"""Implements a HD44780 character LCD connected via pyboard GPIO pins."""

from pyb import Pin, delay, millis
from pyb_gpio_lcd import GpioLcd

# Wiring used for this example:
#
#  1 - Vss (aka Ground) - Connect to one of the ground pins on you pyboard.
#  2 - VDD - I connected to VIN which is 5 volts when your pyboard is powered via USB
#  3 - VE (Contrast voltage) - I'll discuss this below
#  4 - RS (Register Select) connect to Y12 (as per call to GpioLcd)
#  5 - RW (Read/Write) - connect to ground
#  6 - EN (Enable) connect to Y11 (as per call to GpioLcd)
#  7 - D0 - connect to Y1 (as per call to GpioLcd)
#  8 - D1 - connect to Y2 (as per call to GpioLcd)
#  9 - D2 - connect to Y3 (as per call to GpioLcd)
# 10 - D3 - connect to Y4 (as per call to GpioLcd)
# 11 - D4 - connect to Y5 (as per call to GpioLcd)
# 12 - D5 - connect to Y6 (as per call to GpioLcd)
# 13 - D6 - connect to Y7 (as per call to GpioLcd)
# 14 - D7 - connect to Y8 (as per call to GpioLcd)
# 15 - A (BackLight Anode) - Connect to VIN
# 16 - K (Backlight Cathode) - Connect to Ground
#
# On 14-pin LCDs, there is no backlight, so pins 15 & 16 don't exist.
#
# The Contrast line (pin 3) typically connects to the center tap of a
# 10K potentiometer, and the other 2 legs of the 10K potentiometer are
# connected to pins 1 and 2 (Ground and VDD)
#
# The wiring diagram on the following page shows a typical "base" wiring:
# http://www.instructables.com/id/How-to-drive-a-character-LCD-displays-using-DIP-sw/step2/HD44780-pinout/
# Add to that the EN, RS, and D0-D7 lines.


def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    lcd = GpioLcd(rs_pin=Pin.board.Y12,
                  enable_pin=Pin.board.Y11,
                  d0_pin=Pin.board.Y1,
                  d1_pin=Pin.board.Y2,
                  d2_pin=Pin.board.Y3,
                  d3_pin=Pin.board.Y4,
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
