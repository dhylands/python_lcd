lcd and i2c_lcd
===============

Python code for talking to character based LCDs.

The I2c_Lcd class allows for talking to i2c based LCDs.

This was tested on a BeagleBone Black using a 2 x 16 LCD with an i2c
module similar to this one:
http://arduino-info.wikispaces.com/LCD-Blue-I2C

This code was adapted from some C code that I had written previously for
the AVR.

To install on your BBB:
git clone https://github.com/dhylands/python_lcd.git
cd python_lcd
sudo pip install -e .

And to test:
sudo lcd/i2c_lcd.py

Since my LCD was a 5v device, I used a level converter to convert from BBB's
3.3v to the LCD's 5v.

Some photos of my setup are here:
https://picasaweb.google.com/115853040635737241756/PythonI2CLCD?authkey=Gv1sRgCLyZoJ3_uPjiXA

Coming from the BeagleBone Black the wire colors are:
Black:  P9-1  GND
Red:    P9-3  3.3v
Orange: P9-5  5v
Yellow: P9-19 SCL
White:  P9-20 SDA

And the colors going to the LCD are:
Black:  GND
Red:    5v
White:  SDA
Yellow: SCL

I used a SparkFun level shifter:
https://www.sparkfun.com/products/8745
This particular level shifter is no longer sold, and can be replaced with
https://www.sparkfun.com/products/11978 or
https://www.sparkfun.com/products/12009 or
https://www.sparkfun.com/products/11771 or  
https://www.sparkfun.com/products/11955

Any suitable level shifter should work fine.
