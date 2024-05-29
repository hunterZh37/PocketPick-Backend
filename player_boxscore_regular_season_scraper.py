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

def convert_to_dict(headers,data): 
    return dict(zip(headers, data))

def scrape_player_boxscore():
    options = Options()
    options.headless = True
    driver_path = '/opt/homebrew/bin/chromedriver'
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()

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
        for i in range(page_number):
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
                    row_data = [cell.text[-3:] if '@' in cell.text or 'vs.' in cell.text else cell.text for cell in cells]
                    row_data = convert_to_dict(headers,row_data)
                    #print(row_data)
                    data.append(row_data)
            
            
                next_button = find_next_button(driver.find_element(By.CSS_SELECTOR, "div.Crom_cromSettings__ak6Hd"))
                # print("next button: ", next_button.get_attribute('innerHTML'))
                actions = ActionChains(driver)
                actions.move_to_element(next_button).click().perform()
                time.sleep(8)
            else:
                print("Table not found.")
            
            # print("data: ", data)  

        # print(data)

        return data
    except Exception as e:
        print("TimeoutException: Table not found within the specified wait time.", e)

    finally:
        # Always close the driver
        driver.quit()