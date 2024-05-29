from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os
from datetime import datetime
from supabase import create_client, Client

SUPABASE_URL="https://nnbdlnflutymeudqdaqc.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5uYmRsbmZsdXR5bWV1ZHFkYXFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQwMjI5NjQsImV4cCI6MjAyOTU5ODk2NH0.vYc5COQvFK4QDF_lGpXLHltVRoJEtR1B8T8wUQHHXPc"
url = SUPABASE_URL
key = SUPABASE_KEY

# Set up the WebDriver with Chrome options
options = Options()
options.add_experimental_option('prefs', {
    "download.default_directory": os.getcwd(),  # Change default directory for downloads
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


def format(filename):
   # Replace with your file path
   df = pd.read_csv(filename)

   # Define the new column names
   new_column_names = [
      'name', 'team', 'opponent_team', 'dk_points', 'dk_over', 'dk_under',
      'fd_points', 'fd_over', 'fd_under', 'mgm_points', 'mgm_over', 'mgm_under',
      'br_points', 'br_over', 'br_under'
   ]

   # Rename the columns
   df.columns = new_column_names
   # Remove the first row
   df = df.drop(index=0)
   # Save the updated DataFrame to a new CSV file
   df.to_csv(filename, index=False)

# Function to download and rename the file
def download_and_rename_file():
    # Initialize the WebDriver using WebDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get('https://www.rotowire.com/betting/nba/player-props.php')

        # Allow time to enter password
        time.sleep(30)  

        # Locate the download button using the given selector and click it
        download_button = driver.find_element(By.CSS_SELECTOR, '#props-pts > div.export-bar > div.export-buttons > button.export-button.is-csv')
        download_button.click()

        # download time
        time.sleep(10)  

        # Locate the downloaded file and rename it to the current date and time
        downloaded_filename = max([f for f in os.listdir(os.getcwd())], key=os.path.getctime)
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_filename = f"props_{current_time}.csv"
        os.rename(downloaded_filename, new_filename)
        format(new_filename)

        # Upload the renamed file to Supabase storage -- TODO:FIX
      #   with open(new_filename, "rb") as file:
      #       supabase.storage().from_('odds').upload(new_filename, file)

    finally:
        # Close the WebDriver
        driver.quit()

# Main loop to run the function every 6 hours
while True:
    download_and_rename_file()
    time.sleep(6 * 3600)  # Sleep for 6 hours

