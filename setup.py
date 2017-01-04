from distutils.core import setup

setup(
    name='python_lcd',
    version='0.1.0',
    author='Dave Hylands',
    author_email='dhylands@gmail.com',
    packages=['lcd'],
    scripts=[],
    url='https://github.com/dhylands/python_lcd/',
    license='LICENSE',
    description='Python library for HD44780 compatible character based LCDs.',
    long_description=open('README.md').read(),
    install_requires=[
        'smbus'
    ],
)
