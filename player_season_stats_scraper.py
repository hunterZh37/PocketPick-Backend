# https://www.nba.com/stats/players/traditional?dir=A&sort=TEAM_ABBREVIATION


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import utility

# "player_id"

headers = [
    "player_id","name", "team", "age", "gp", "wins", "losses", "min", "pts", "fgm", "fga", 
    "fgperc", "3pm", "3pa", "3perc", "ftm", "fta", "ftperc", "orpg", "drpg", "reb", "ast", 
    "tov", "stl", "blk", "pf", "fp", "dd","td", "pm" 
]

def scrape_player_season_stats():
    try:
        options = Options()
        options.headless = True
        driver_path = '/opt/homebrew/bin/chromedriver'
        s = Service(driver_path)
        driver = webdriver.Chrome(service=s, options=options)
        driver.maximize_window()
        driver.get("https://www.nba.com/stats/players/traditional")
        wait = WebDriverWait(driver, 10)
        page_num_selector = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select.DropDown_select__4pIg9")))
        page_num_selector = driver.find_elements(By.CSS_SELECTOR, "select.DropDown_select__4pIg9")[-1]
        page_num = page_num_selector.find_elements(By.CSS_SELECTOR, "option")[-1].text
        print(page_num)

        # subtables = []
        data = []
        player_id = 1
        for i in range(int(page_num)):
            table = driver.find_element(By.CSS_SELECTOR, "table.Crom_table__p1iZz")
    
            for row in table.find_elements(By.XPATH, ".//tbody/tr"):
                row_data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
                row_data[0] = player_id
                player_id += 1
                row_data = utility.convert_to_dict(headers,row_data) 
                print(row_data)
                data.append(row_data)

            actions = ActionChains(driver)
            button = (driver.find_elements(By.CSS_SELECTOR, "button.Pagination_button__sqGoH"))[1]
            actions.move_to_element(button).click().perform()

        # print(data)   
        return data    

    except Exception as e:
        print(e)

    finally: 
        driver.quit()


