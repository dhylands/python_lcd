"""Implements a HD44780 character LCD connected via Onion Omega GPIO pins."""

from onion_lcd_gpio import GpioLcd
from time import sleep, clock #Note: clock removed in python 3.8 (however onion distributes python 3.4)

# https://docs.onion.io/omega2-docs/gpio-python-module.html#gpio-python-module
# requires a python3 modification of the current standard onionGpio (as of 2021-11-20)
from onionGpio import OnionGpio

# Wiring used for this example:
# tested with Onion omega2+
#
#  1 - Vss (aka Ground) - Connect to one of the ground pins on you pyboard.
#  2 - VDD - I connected to VIN which is 5 volts when your pyboard is powered via USB
#  3 - VE (Contrast voltage) - I'll discuss this below
#  4 - RS (Register Select) connect to gpio pin 2 (as per call to GpioLcd)
#  5 - RW (Read/Write) - connect to ground
#  6 - EN (Enable) connect to gpio pin 3 (as per call to GpioLcd)
#  7 - D0 - leave unconnected
#  8 - D1 - leave unconnected
#  9 - D2 - leave unconnected
# 10 - D3 - leave unconnected
# 11 - D4 - connect to gpio pin 0 (as per call to GpioLcd)
# 12 - D5 - connect to gpio pin 1 (as per call to GpioLcd)
# 13 - D6 - connect to gpio pin 6 (as per call to GpioLcd)
# 14 - D7 - connect to gpio pin 19 (as per call to GpioLcd)
# 15 - A (BackLight Anode) - Connect to VIN
# 16 - K (Backlight Cathode) - Connect to Ground
#
# On 14-pin LCDs, there is no backlight, so pins 15 & 16 don't exist.
#
# The Contrast line (pin 3) typically connects to the center tap of a
# 10K potentiometer, and the other 2 legs of the 10K potentiometer are
# connected to pins 1 and 2 (Ground and VDD)
#
# See: https://docs.onion.io/omega2-docs/using-gpios.html#boot-pins
# for more info on which pins can be used freely
# note that pins must be in gpio mode, see the onion docs
#
#


def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    lcd = GpioLcd(rs_pin=OnionGpio(2),
                  enable_pin=OnionGpio(3),
                  d4_pin=OnionGpio(0),
                  d5_pin=OnionGpio(1),
                  d6_pin=OnionGpio(6),
                  d7_pin=OnionGpio(19),
                  num_lines=2, num_columns=16)
    lcd.putstr("It Works!\nSecond Line\nThird Line\nFourth Line")
    sleep(3)
    lcd.clear()
    count = 0
    while True:
        lcd.move_to(0, 0)
        lcd.putstr("%7d" % (int(round(clock(),6)*1E6) // 1000))
        sleep(1)
        count += 1

if __name__ == '__main__':
    test_main()
