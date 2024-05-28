# https://www.nba.com/stats/players/traditional?sort=W&dir=-1

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import pytz
import schedule
import json

try: 
    

except Exception as e:
    print(e)

finally: 
    driver.quit()


