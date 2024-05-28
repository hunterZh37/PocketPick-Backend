from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def get_traditional_stats(driver):
        driver.get("https://www.nba.com/stats/players/traditional")
        # Wait for the page to load and the button to be clickable
        wait = WebDriverWait(driver, 5)
        page_num_selector = driver.find_elements(By.CSS_SELECTOR, "select.DropDown_select__4pIg9")[-1]
        page_num = page_num_selector.find_elements(By.CSS_SELECTOR, "option")[-1].text
        rows = []
        for i in range(int(page_num)):
            table = driver.find_element(By.CSS_SELECTOR, "table.Crom_table__p1iZz")
            header = [header.text for header in table.find_elements(By.XPATH, ".//thead/tr/th") if header.text != ""] 
            header[0] = "ID"
            for row in table.find_elements(By.XPATH, ".//tbody/tr"):
                row_data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
                rows.append(dict(zip(header, row_data)))
            if i != int(page_num) - 1:
                actions = ActionChains(driver)
                button_container = driver.find_element(By.CSS_SELECTOR, "div.Pagination_buttons__YpLUe")
                button = (driver.find_elements(By.CSS_SELECTOR, "button.Pagination_button__sqGoH"))[1]
                actions.move_to_element(button_container).click(button).perform()
        return rows