import os
import platform
import subprocess
import zipfile
from selenium import webdriver
import requests
from selenium.webdriver.chrome.service import Service

file_path= str(os.getcwd()) + '/chrome/chromedriver-mac-arm64/chromedriver'
service = Service(executable_path=file_path)
driver = webdriver.Chrome(service=service)