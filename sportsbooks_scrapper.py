# This is the only code required to download the csv from https://www.rotowire.com/betting/nba/player-props.php:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os

# Set up the WebDriver with Chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": os.getcwd(),  # Change default directory for downloads
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Manually specify the path to the ChromeDriver
chromedriver_path = '/path/to/chromedriver'  # Update this with your actual path

driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

try:
    # Navigate to the website
    driver.get('https://www.rotowire.com/betting/nba/player-props.php')

    # Allow the page to load completely
    time.sleep(5)  # Adjust the sleep time if necessary

    # Locate the download button using the given selector and click it
    download_button = driver.find_element(By.CSS_SELECTOR, '#props-pts > div.export-bar > div.export-buttons > button.export-button.is-csv')
    download_button.click()

    # Allow time for the file to download
    time.sleep(10)  # Adjust the sleep time if necessary

finally:
    # Close the WebDriver
    driver.quit()