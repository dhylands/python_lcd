lcd and i2c_lcd
===============

Python code for talking to HD44780 compatible character based dot matrix LCDs.

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

Files
=====

| File                          | Description                           |
| -----                         | -----------                           |
| esp8266_i2c_lcd.py            | ESP8266 PCF8574 I2C HAL               |
| esp8266_i2c_lcd_test.py       | ESP8266 test using PCF8574 backpack   |
| i2c_lcd.pyb                   | Linux PCF8574 I2C HAL                 |
| i2c_lcd_test.pyb              | Linux test using PCF8574 backpack     |
| lcd.py                        | Core logic                            |
| nodemcu_gpio_lcd.py           | NodeMCU GPIO HAL                      |
| nodemcu_gpio_lcd_test.py      | NodeMCU test using 4-bit GPIO         |
| pyb_gpio_lcd.py               | Pyboard GPIO HAL                      |
| pyb_gpio_lcd_test8.py         | Pyboard test using 8-bit GPIO         |
| pyb_gpio_lcd_test.py          | Pyboard test using 4-bit GPIO         |
| pyb_i2c_adafruit_lcd.py       | Pyboard MCP23008 I2C HAL              |
| pyb_i2c_adafruit_lcd_test.py  | Pyboard test using Adafruit backpack  |
| pyb_i2c_lcd.py                | Pyboard PCF8574 I2C HAL               |
| pyb_i2c_lcd_test.py           | Pyboard test using PCF8574 backpack   |


The files which end in **_test.py** are examples which show how the corresponding
file is used.

**i2c_lcd.py** was tested on a [BeagleBone Black](https://beagleboard.org/black) using a 2 x 16 LCD with an I2C
module similar to [this one](http://arduino-info.wikispaces.com/LCD-Blue-I2C).

This code was adapted from some C code that I had written previously for
the AVR.

To install on your BBB:
```bash
git clone https://github.com/dhylands/python_lcd.git
cd python_lcd
sudo pip install -e .
```

And to test:
```bash
sudo lcd/i2c_lcd.py
```

Since my LCD was a 5v device, I used a level converter to convert from BBB's
3.3v to the LCD's 5v.

I put together some
[photos here] (https://picasaweb.google.com/115853040635737241756/PythonI2CLCD?authkey=Gv1sRgCLyZoJ3_uPjiXA)

Coming from the BeagleBone Black the wire colors are:
```
Color  Pin   Name
------ ----- ------
Black  P9-1  GND
Red    P9-3  3.3v
Orange P9-7  SYS_5V
Yellow P9-19 SCL
White  P9-20 SDA
```

The photo shows Orange connected to P9-5. I discovered that P9-7 is controlled
by the onboard voltage regulators, so when you do a "sudo poweroff" then
SYS_5V drops to 0v when the BBB is powered off. P9-5 (VDD_5V) remains at
5v after the BBB is powered off.

And the colors going to the LCD are:
```
Color  Name
------ ----
Black  GND
Red    5v
White  SDA
Yellow SCL
```

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
