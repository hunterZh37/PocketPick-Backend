import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import utility

import utility

# Setup Chrome options

def find_number_of_pages(data):
    temp = data.find_element(By.CSS_SELECTOR, "div.Pagination_content__f2at7.Crom_cromSetting__Tqtiq")
    
    total_pages = temp.find_element(By.XPATH, './div[contains(text(), "of ")]').text.strip()
    total_pages = int(total_pages.replace("of ", "")) # Remove "of "
    # print(total_pages)
    return total_pages


def find_next_button(data):
    temp = data.find_element(By.CSS_SELECTOR, "div.Pagination_content__f2at7.Crom_cromSetting__Tqtiq")
    temp = temp.find_element(By.XPATH, '//button[@title="Next Page Button" and @class="Pagination_button__sqGoH"]')
   
    # next_button = WebDriverWait(driver, 10).until(
    #                 EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Pagination_button__sqGoH")))
                
    # next_button = temp.find_element(By.CSS_SELECTOR, "button.Pagination_button__sqGoH")
    return temp


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

# def scrape_player_boxscore():
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
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.Crom_cromSettings__ak6Hd"))
    )

    page_number = find_number_of_pages(driver.find_element(By.CSS_SELECTOR, "div.Crom_cromSettings__ak6Hd"))
    # print(page_number)
    


    data = []
    for i in range(10):
        print("Page number: ", i)
        table = driver.find_element(By.CSS_SELECTOR, "table.Crom_table__p1iZz")
        if table:
            table_data = []   
            print("Table found.", table)
            tbody = table.find_element(By.CSS_SELECTOR, "tbody.Crom_body__UYOcU")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
        
            for row in rows:
                # Find all cells in the row
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text for cell in cells]
                print(row_data)
                # fix the json format.

            data.append(parse_data_into_json(headers, table_data))
            next_button = find_next_button(driver.find_element(By.CSS_SELECTOR, "div.Crom_cromSettings__ak6Hd"))
            # print("next button: ", next_button.get_attribute('innerHTML'))
            actions = ActionChains(driver)
            actions.move_to_element(next_button).click().perform()
            time.sleep(8)
        else:
            print("Table not found.")

    old_boxscore = utility.load_previous_file("player_boxscore_regular_season.json")
    changes = utility.detect_changes(data, old_boxscore)
    # print(changes)

    if changes:
        utility.notify_changes(changes)
        # delete_schedule_data()
        utility.save_file(data, "player_boxscore_regular_season.json") 
        # insert_schedule_data(player_boxscore_output)
    else:
        print("No changes detected")


    # print(data)

    # return data
except Exception as e:
    print("TimeoutException: Table not found within the specified wait time.", e)

finally:
    # Always close the driver
    driver.quit()