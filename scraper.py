import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class Scraper:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.driver_path = '/opt/homebrew/bin/chromedriver'
        self.s = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=self.s, options=self.options)
        
    def get_schedule(self):
        self.driver.get("https://www.nba.com/schedule")
        time.sleep(5)
        self.driver.minimize_window()
        schedule = self.driver.find_elements(By.CSS_SELECTOR, "div.ScheduleDay_sd__GFE_w")
        game_list = []
        header = ["date", "time", "home_team", "opponent_team"]
        for day in schedule:
            date = day.find_element(By.CSS_SELECTOR, "h4.ScheduleDay_sdDay__3s2Xt").text
            games = day.find_elements(By.CSS_SELECTOR, "div.ScheduleGame_sg__RmD9I")
            for game in games:
                timing = game.find_element(By.CSS_SELECTOR, "span.ScheduleStatusText_base__Jgvjb").text
                teams = game.find_elements(By.CSS_SELECTOR, "div.ScheduleGame_sgTeam__TEPZa")
                teams = [t.text for t in teams]
                new_game = [date, timing, teams[0], teams[1]]
                game_list.append(new_game)
        df = pd.DataFrame(game_list, columns=header)
        return df
    
    def get_traditional_stats(self):
        self.driver.get("https://www.nba.com/stats/players/traditional")
        # Wait for the page to load and the button to be clickable
        wait = WebDriverWait(self.driver, 5)
        actions = ActionChains(self.driver)
        button_container = self.driver.find_element(By.CSS_SELECTOR, "div.Pagination_buttons__YpLUe")
        button = (self.driver.find_elements(By.CSS_SELECTOR, "button.Pagination_button__sqGoH"))[1]
        actions.move_to_element(button_container).click(button).perform()
        
        
        table = self.driver.find_element(By.CSS_SELECTOR, "table.Crom_table__p1iZz")
        header = [header.text for header in table.find_elements(By.XPATH, ".//thead/tr/th") if header.text != ""]   
        
        rows = []
        for row in table.find_elements(By.XPATH, ".//tbody/tr"):
            row_data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            rows.append(row_data)
        df = pd.DataFrame(rows, columns=header)
        return df
    def close(self):
        self.driver.quit()