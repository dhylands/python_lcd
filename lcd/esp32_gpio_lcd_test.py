"""Implements a HD44780 character LCD connected via ESP32 GPIO pins."""

from machine import Pin
from esp32_gpio_lcd import GpioLcd
from utime import sleep_ms, ticks_ms

# Wiring used for this example:
#
#  1 - Vss (aka Ground) - Connect to one of the ground pins on you pyboard.
#  2 - VDD - I connected to VIN which is 5 volts when your pyboard is powered via USB
#  3 - VE (Contrast voltage) - I'll discuss this below
#  4 - RS (Register Select) connect to G4 (as per call to GpioLcd)
#  5 - RW (Read/Write) - connect to ground
#  6 - EN (Enable) connect to G11 (as per call to GpioLcd)
#  7 - D0 - leave unconnected
#  8 - D1 - leave unconnected
#  9 - D2 - leave unconnected
# 10 - D3 - leave unconnected
# 11 - D4 - connect to G5 (as per call to GpioLcd)
# 12 - D5 - connect to G18 (as per call to GpioLcd)
# 13 - D6 - connect to G21 (as per call to GpioLcd)
# 14 - D7 - connect to G22 (as per call to GpioLcd)
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
# Add to that the EN, RS, and D4-D7 lines.


def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    lcd = GpioLcd(rs_pin=Pin(4),
                  enable_pin=Pin(17),
                  d4_pin=Pin(5),
                  d5_pin=Pin(18),
                  d6_pin=Pin(21),
                  d7_pin=Pin(22),
                  num_lines=2, num_columns=20)
    lcd.putstr("It Works!\nSecond Line\nThird Line\nFourth Line")
    sleep_ms(3000)
    lcd.clear()
    count = 0
    while True:
        lcd.move_to(0, 0)
        lcd.putstr("%7d" % (ticks_ms() // 1000))
        sleep_ms(1000)
        count += 1
