
# Make sure you have upgraded version of pip
Windows
```
py -m pip install --upgrade pip
```

Linux/MAC OS
```
python3 -m pip install --upgrade pip
```

## Install
```
pip install chromedriver-auto

or 

pip3 install chromedriver-auto
```

## This package works for chrome version >= 115.0.5790.102
Recently(24 july 2023) Google has published a new website for providing chromedriver for newer versions of CHROME BROWSER.
Details: https://googlechromelabs.github.io/chrome-for-testing/ 

first it checks, if a chromedriver is already there or not. If no chromedriver or version miss-match found, it will download chromedriver automatically from the official website.

Use Code:


```
from chromedriver_auto.driver_ready import *
driver.get('https://www.google.com')
```
