import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
options = Options()
options.headless = True
driver_path = '/opt/homebrew/bin/chromedriver'
s = Service(driver_path)
driver = webdriver.Chrome(service=s, options=options)

try:
    # Open the webpage
    driver.get("https://www.nba.com/stats/players/boxscores?SeasonType=Regular+Season")

    # Increase wait time and verify correct selector
    wait = WebDriverWait(driver, 20)
    table = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.Crom_table__p1iZz")))

    # Verify if the table is found
    if table:
        print("Table found.", table)
        headers = [header.text for header in table.find_elements(By.XPATH, ".//thead/tr/th")]
        # date = day.find_element(By.CSS_SELECTOR, "h4.ScheduleDay_sdDay__3s2Xt").text
        # games = day.find_elements(By.CSS_SELECTOR, "div.ScheduleGame_sg__RmD9I")
        print("Headers:", headers)  # Debug print
    else:
        print("Table not found.")

except Exception as e:
    print("TimeoutException: Table not found within the specified wait time.", e)

finally:
    # Always close the driver
    driver.quit()



# # Extract column headers
# headers = [header.text for header in table.find_elements(By.XPATH, ".//thead/tr/th")]
# print("Headers:", headers)  # Debug print

# # Extract rows
# rows = []
# for row in table.find_elements(By.XPATH, ".//tbody/tr"):
#     row_data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
#     rows.append(row_data)
#     print("Row data:", row_data)  # Debug print

# # Check if headers and rows were extracted correctly
# if not headers or not rows or all(not row for row in rows):
#     print("Error: Could not extract table data. Please check the XPath or table structure.")
# else:
#     # Create a DataFrame
#     df = pd.DataFrame(rows, columns=headers)

#     # Save to CSV
#     df.to_csv("nba_boxscores.csv", index=False)

#     print("CSV file created successfully.")

# # Close the WebDriver
# driver.quit()