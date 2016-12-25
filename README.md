lcd and i2c_lcd
===============

Python code for talking to character based LCDs.

The I2c_Lcd class allows for talking to i2c based LCDs. There are also variants
of the code for MicroPython. All of the files which start with pyb were tested
on the pyboard.

Files
=====

| File                          | Description                           |
| -----                         | -----------                           |
| lcd.py                        | Core logic                            |
| i2c_lcd.pyb                   | Linux I2C HAL                         |
| pyb_gpio_lcd.py               | Pyboard GPIO HAL                      |
| pyb_gpio_lcd_test8.py         | Pyboard test using 8-bit GPIO         |
| pyb_gpio_lcd_test.py          | Pyboard test using 4-bit GPIO         |
| pyb_i2c_adafruit_lcd.py       | Pyboard I2C HAL for Adafruit backpack |
| pyb_i2c_adafruit_lcd_test.py  | Test for Adafruit backpack            |
| pyb_i2c_lcd.py                | Pyboard I2C HAL for PCF8574 backpack  |
| pyb_i2c_lcd_test.py           | Test for PCF8574 backpack             |
| nodemcu_gpio_lcd.py           | NodeMCU GPIO HAL                      |
| nodemcu_gpio_lcd_test.py      | NodeMCU test using 4-bit GPIO         |


The files which end in _test.py are examples which show how the corresponding
file is used.

i2c_lcd.py was tested on a BeagleBone Black using a 2 x 16 LCD with an i2c
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
