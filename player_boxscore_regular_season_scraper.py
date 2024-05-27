import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import utility

# Setup Chrome options

def parse_data_into_json(headers,data):
     parsed_data = []
     for row in data:
        player_stats = []
        for header, value in zip(headers, row):
            if isinstance(value, str) and ('@' in value or 'vs.' in value):
                value = value[-3:]
            player_stats.append({header: value})
        parsed_data.append(player_stats)
     return parsed_data

def scrape_player_boxscore():
    options = Options()
    options.headless = True
    driver_path = '/opt/homebrew/bin/chromedriver'
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=options)

    headers = [
        "name", "team", "opponent_team", "date", "result",
        "minutes", "pts", "fgm", "fga", "fgperc",
        "3pm", "3pa", "3perc",
        "ftm", "fta", "ftperc", "oreb", "dreb",
        "reb", "ast", "stl", "blk", "to", "pf", "plus_minus",
        "per"
    ]

    try:
        # Open the webpage
        driver.get("https://www.nba.com/stats/players/boxscores?SeasonType=Regular+Season")

        # Increase wait time and verify correct selector
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.Crom_table__p1iZz"))
        )
        
        table = driver.find_element(By.CSS_SELECTOR, "table.Crom_table__p1iZz")

        # Verify if the table is found
        
        if table:
            print("Table found.", table)
            tbody = table.find_element(By.CSS_SELECTOR, "tbody.Crom_body__UYOcU")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            table_data = []   
            for row in rows:
                # Find all cells in the row
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text for cell in cells]
                table_data.append(row_data)

            return parse_data_into_json(headers, table_data)   
        else:
            print("Table not found.")

    except Exception as e:
        print("TimeoutException: Table not found within the specified wait time.", e)

    finally:
        # Always close the driver
        driver.quit()

