lcd_api and i2c_lcd
===============

Python code for talking to HD44780 compatible character based dot matrix LCDs.

## Other ports

This code is synchronous. Peter Hinch put together an async driver for
the HD77480 over [here](https://github.com/peterhinch/micropython-async/tree/master/HD44780).

This library is based off of a C version that I wrote, which can be found
[here](https://github.com/dhylands/projects/blob/master/common/lcd-api.c)
(also look for files in the same directory which start with lcd).

Nic created a C# port of this library which can be found [here](https://github.com/OfItselfSo/CS_LCD).

## Communicating with the LCD

You can communicate with the LCDs using either 4 or 8 GPIO pins.

Alternatively, the I2C classes implement 8-bit GPIO expander boards
[PCF8574](http://www.ti.com/lit/ds/symlink/pcf8574.pdf) and
[MCP23008](http://www.microchip.com/wwwproducts/en/MCP23008)
which reduces the number of required GPIO pins to two (SCL, SDA).
The boards usually mount behind the LCDs and are commonly called "backpacks".

The most commonly used display is a "1602" or "16x2", which features 16 columns
and 2 rows of characters. There are also other LCDs using the same HD44780
controller. eg. 8x2, 16x1, 16x4, 20x2, 20x4, 40x1, 40x2. Each come in various
backlight and pixel colours.

There are also variants of the code for [MicroPython](http://micropython.org/).
All of the files which start with **pyb_** were tested on the
[pyboard](https://store.micropython.org/store/#/products/PYBv1_1).
Files starting with **esp8266_** were tested on a
[WeMos D1 Mini](https://www.wemos.cc/product/d1-mini.html).
Files starting with **nodemcu_** were tested on a
[NodeMCU development board](https://en.wikipedia.org/wiki/NodeMCU).
The files containing **adafruit_lcd** were tested on an Adafruit
[I2C / SPI character LCD backpack](https://www.adafruit.com/product/292)

## Tutorial

Giuseppe Cassibba wrote up a [tutorial](https://peppe8o.com/using-i2c-lcd-display-with-raspberry-pi-pico-and-micropython) which demonstrates connecting an I2C LCD to a Raspberry Pi Pico.

## Files

| File                          | Description                           |
| -----                         | -----------                           |
| esp32_gpio_lcd.py             | ESP32 GPIO HAL                        |
| esp32_gpio_lcd_test.py        | ESP32 test using 4-bit GPIO           |
| esp8266_i2c_lcd.py            | ESP8266 PCF8574 I2C HAL               |
| esp8266_i2c_lcd_test.py       | ESP8266 test using PCF8574 backpack   |
| i2c_lcd.py                    | Linux PCF8574 I2C HAL                 |
| i2c_lcd_test.py               | Linux test using PCF8574 backpack     |
| lcd_api.py                    | Core logic                            |
| machine_i2c_lcd.py            | Pyboard machine.I2C PCF8574 backpack  |
| machine_i2c_lcd_test.py       | Test for machine.I2C PCF8574 backpack |
| nodemcu_gpio_lcd.py           | NodeMCU GPIO HAL                      |
| nodemcu_gpio_lcd_test.py      | NodeMCU test using 4-bit GPIO         |
| pyb_gpio_lcd.py               | Pyboard GPIO HAL                      |
| pyb_gpio_lcd_test8.py         | Pyboard test using 8-bit GPIO         |
| pyb_gpio_lcd_test.py          | Pyboard test using 4-bit GPIO         |
| pyb_i2c_adafruit_lcd.py       | Pyboard MCP23008 I2C HAL              |
| pyb_i2c_adafruit_lcd_test.py  | Pyboard test using Adafruit backpack  |
| pyb_i2c_grove_rgb_lcd.py      | Pyboard Grove I2C RGB LCD HAL         |
| pyb_i2c_grove_rgb_lcd_test.py | Pyboard test using Grove I2C RGB LCD  |
| pyb_i2c_lcd.py                | Pyboard PCF8574 I2C HAL               |
| pyb_i2c_lcd_test.py           | Pyboard test using PCF8574 backpack   |


The files which end in **_test.py** are examples which show how the corresponding
file is used.

**i2c_lcd.py** was tested on a [BeagleBone Black](https://beagleboard.org/black) using a 2 x 16 LCD with an I2C
module similar to [this one](http://arduino-info.wikispaces.com/LCD-Blue-I2C).

To install on your BBB:
```bash
git clone https://github.com/dhylands/python_lcd.git
cd python_lcd
sudo pip install -e .
```

And to test:
```bash
sudo lcd/i2c_lcd_test.py
```

Since my LCD was a 5v device, I used a level converter to convert from BBB's
3.3v to the LCD's 5v.

I put together some
[photos here] (https://picasaweb.google.com/115853040635737241756/PythonI2CLCD?authkey=Gv1sRgCLyZoJ3_uPjiXA)

Coming from the BeagleBone Black the wire colors are:

| Color  | Pin   | Name   |
| ------ | ----- | ------ |
| Black  | P9-1  | GND    |
| Red    | P9-3  | 3.3v   |
| Orange | P9-7  | SYS_5V |
| Yellow | P9-19 | SCL    |
| White  | P9-20 | SDA    |

The photo shows Orange connected to P9-5. I discovered that P9-7 is controlled
by the onboard voltage regulators, so when you do a "sudo poweroff" then
SYS_5V drops to 0v when the BBB is powered off. P9-5 (VDD_5V) remains at
5v after the BBB is powered off.

And the colors going to the LCD are:

| Color  | Name |
| ------ | ---- |
| Black  | GND  |
| Red    | 5v   |
| White  | SDA  |
| Yellow | SCL  |

I used a [SparkFun level shifter](https://www.sparkfun.com/products/8745)
(this particular model is no longer available).

Some examples of other level shifters which could be used:
* [Logic Level Converter](https://www.sparkfun.com/products/11978)
* [Logic Level Converter Bi-Directional](https://www.sparkfun.com/products/12009)
* [Voltage-Level Translator - TXB0104 Breakout](https://www.sparkfun.com/products/11771)
* [PCA9306 Level Translator Breakout](https://www.sparkfun.com/products/11955)
* [4-channel I2C-safe Bi-directional Logic Level Converter - BSS138](http://www.adafruit.com/products/757)
* [8-channel Bi-directional Logic Level Converter - TXB0108](http://www.adafruit.com/products/395)

I found a circuit mentioned in [this Google+ post](https://plus.google.com/101619328411109842819/posts/5dPjmvRwhXH)
and thought I would include it here, since it's related to the LCDs these drivers interface with.
![LCD Schematic](/simplest-lcd-supply.png)

The circuit allows for digitally controlling the contrast via PWM and also controlling
the backlight brightness via PWM.

## Custom characters

The HD44780 displays come with 3 possible CGROM font sets. Japanese, European and Custom.
Test which you have using:

```
lcd.putchar(chr(247))
```

If you see Pi (π), you have a Japanese A00 ROM.
If you see a division sign (÷), you have a European A02 ROM.

Characters match ASCII characters in range 32-127 (0x20-0x7F) with a few exceptions:

* 0x5C is a Yen symbol instead of backslash
* 0x7E is a right arrow instead of tilde
* 0x7F is a left arrow instead of delete

Only the ASCII characters are common between the two ROMs 32-125 (0x20-0x7D)
Refer to the HD44780 datasheet for the table of characters.

The first 8 characters are CGRAM or character-generator RAM.
You can specify any pattern for these characters.

To design a custom character, start by drawing a 5x8 grid.
I use dots and hashes as it's a lot easier to read than 1s and 0s.
Draw pixels by replacing dots with hashes.
Where possible, leave the bottom row unpopulated as it may be occupied by the underline cursor.

```
Happy Face (where .=0, #=1)
.....
.#.#.
.....
..#..
.....
#...#
.###.
.....
```

To convert this into a bytearray for the custom_char() method, you need to add each row of 5 pixels to least significant bits of a byte (the right side).

```
Happy Face (where .=0, #=1)
..... == 0b00000 == 0x00
.#.#. == 0b01010 == 0x0A
..... == 0b00000 == 0x00
..#.. == 0b00100 == 0x04
..... == 0b00000 == 0x00
#...# == 0b10001 == 0x11
.###. == 0b01110 == 0x0E
..... == 0b00000 == 0x00
```

Next, add each byte from top to bottom to a new byte array and pass to custom_char() with location 0-7.

```
happy_face = bytearray([0x00,0x0A,0x00,0x04,0x00,0x11,0x0E,0x00])
lcd.custom_char(0, happy_face)
```

`custom_char()` does not print anything to the display. It only updates the CGRAM.
To display the custom characters, use putchar() with chr(0) through chr(7).

```
lcd.putchar(chr(0))
lcd.putchar(b'\x00')
```

Characters are displayed by reference.
Once you have printed a custom character to the lcd, you can overwrite the custom character and all visible instances will also update.
This is useful for drawing animations and graphs, as you only need to print the characters once and then can simply modify the custom characters in CGRAM.

Examples:

```
# smiley faces
happy = bytearray([0x00,0x0A,0x00,0x04,0x00,0x11,0x0E,0x00])
sad = bytearray([0x00,0x0A,0x00,0x04,0x00,0x0E,0x11,0x00])
grin = bytearray([0x00,0x00,0x0A,0x00,0x1F,0x11,0x0E,0x00])
shock = bytearray([0x0A,0x00,0x04,0x00,0x0E,0x11,0x11,0x0E])
meh = bytearray([0x00,0x0A,0x00,0x04,0x00,0x1F,0x00,0x00])
angry = bytearray([0x11,0x0A,0x11,0x04,0x00,0x0E,0x11,0x00])
tongue = bytearray([0x00,0x0A,0x00,0x04,0x00,0x1F,0x05,0x02])

# icons
bell = bytearray([0x04,0x0e,0x0e,0x0e,0x1f,0x00,0x04,0x00])
note = bytearray([0x02,0x03,0x02,0x0e,0x1e,0x0c,0x00,0x00])
clock = bytearray([0x00,0x0e,0x15,0x17,0x11,0x0e,0x00,0x00])
heart = bytearray([0x00,0x0a,0x1f,0x1f,0x0e,0x04,0x00,0x00])
duck = bytearray([0x00,0x0c,0x1d,0x0f,0x0f,0x06,0x00,0x00])
check = bytearray([0x00,0x01,0x03,0x16,0x1c,0x08,0x00,0x00])
cross = bytearray([0x00,0x1b,0x0e,0x04,0x0e,0x1b,0x00,0x00])
retarrow = bytearray([0x01,0x01,0x05,0x09,0x1f,0x08,0x04,0x00])

# battery icons
battery0 = bytearray([0x0E,0x1B,0x11,0x11,0x11,0x11,0x11,0x1F])  # 0% Empty
battery1 = bytearray([0x0E,0x1B,0x11,0x11,0x11,0x11,0x1F,0x1F])  # 16%
battery2 = bytearray([0x0E,0x1B,0x11,0x11,0x11,0x1F,0x1F,0x1F])  # 33%
battery3 = bytearray([0x0E,0x1B,0x11,0x11,0x1F,0x1F,0x1F,0x1F])  # 50%
battery4 = bytearray([0x0E,0x1B,0x11,0x1F,0x1F,0x1F,0x1F,0x1F])  # 66%
battery5 = bytearray([0x0E,0x1B,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])  # 83%
battery6 = bytearray([0x0E,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])  # 100% Full
battery7 = bytearray([0x0E,0x1F,0x1B,0x1B,0x1B,0x1F,0x1B,0x1F])  # ! Error
```
