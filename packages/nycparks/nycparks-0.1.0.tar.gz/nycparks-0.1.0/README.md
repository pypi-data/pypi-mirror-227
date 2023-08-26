
# nycparks

This package contains a collection of tools to help NYC residents make the most of its parks starting with a system that alerts users over text the upcoming tennis court reservation availabilities.


## Setup

Install the package with `pip install nycparks`. Ensure that you are signed into the desktop client of WhatsApp for the messages to send.


## Basic Usage

The default search times are non 9-5 hours listed in `utils/times.py`. Adjust them based on the times you are interested in playing.

To schedule automatic checks, edit the crontab with:

`crontab -e`

And add the following line adjusting the locations, [alert frequency](https://crontab.guru/every-hour), and number based on your needs. The example below is scheduled for every hour and Central Park, McCarren Park, and Sutton East Park.

`0 * * * * reserve -l central -l mccarren -l 'sutton east' -n +11234567890`


# License
MIT License

Copyright (c) [2023] [Austin Botelho]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.