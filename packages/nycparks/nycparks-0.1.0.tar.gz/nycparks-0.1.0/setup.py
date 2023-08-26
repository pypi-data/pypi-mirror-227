# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nycparks', 'nycparks.utils']

package_data = \
{'': ['*'], 'nycparks': ['data/court_info_and_availability_is_saved_here.txt']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=8.1.6,<9.0.0',
 'html5lib>=1.1,<2.0',
 'lxml>=4.9.3,<5.0.0',
 'pandas>=2.0.3,<3.0.0',
 'pynput>=1.7.6,<2.0.0',
 'pywhatkit>=5.4,<6.0',
 'selenium>=4.11.2,<5.0.0',
 'webdriver-manager>=4.0.0,<5.0.0']

entry_points = \
{'console_scripts': ['reserve = nycparks.main:cli']}

setup_kwargs = {
    'name': 'nycparks',
    'version': '0.1.0',
    'description': '',
    'long_description': '\n# nycparks\n\nThis package contains a collection of tools to help NYC residents make the most of its parks starting with a system that alerts users over text the upcoming tennis court reservation availabilities.\n\n\n## Setup\n\nInstall the package with `pip install nycparks`. Ensure that you are signed into the desktop client of WhatsApp for the messages to send.\n\n\n## Basic Usage\n\nThe default search times are non 9-5 hours listed in `utils/times.py`. Adjust them based on the times you are interested in playing.\n\nTo schedule automatic checks, edit the crontab with:\n\n`crontab -e`\n\nAnd add the following line adjusting the locations, [alert frequency](https://crontab.guru/every-hour), and number based on your needs. The example below is scheduled for every hour and Central Park, McCarren Park, and Sutton East Park.\n\n`0 * * * * reserve -l central -l mccarren -l \'sutton east\' -n +11234567890`\n\n\n# License\nMIT License\n\nCopyright (c) [2023] [Austin Botelho]\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
    'author': 'Austin Botelho',
    'author_email': 'austinbotelho@nyu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
