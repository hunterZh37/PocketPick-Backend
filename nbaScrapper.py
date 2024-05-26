# import os
# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Path to the ChromeDriver executable
# driver_path = '/Users/tarankota/PycharmProjects/scraper/chromedriver-mac-x64/chromedriver'

# # Set up the WebDriver
# driver = webdriver.Chrome(executable_path=driver_path)

# # Open the webpage
# driver.get("https://www.nba.com/stats/players/boxscores?SeasonType=Regular+Season")


# Wait for the dynamic content to load
# WebDriverWait(driver, 300).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, "table.Crom_table__p1iZZ"))
# )

# # Extract the table
# table = driver.find_element(By.CSS_SELECTOR, "table.Crom_table__p1iZZ")


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