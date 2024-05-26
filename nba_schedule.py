import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytz
import schedule


# Dictionary mapping NBA team names to their 3-letter abbreviations
team_abbreviations = {
    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BKN',
    'Charlotte Hornets': 'CHA',
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'LA Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Orleans Pelicans': 'NOP',
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHX',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Washington Wizards': 'WAS'
}

# Function to get the abbreviation of a team name
def get_abbreviation(team_name):
    return team_abbreviations.get(team_name, team_name)

def convert_date(date):
    date_obj = datetime.strptime(date, '%A, %B %d')
    current_year = datetime.now().year
    date_obj = date_obj.replace(year=current_year).strftime('%Y-%m-%d')
    return date_obj
  
def get_abbreviation(team_name):
    return team_abbreviations.get(team_name, team_name)

def convert_time(time_str):
     parsed_time= datetime.strptime(time_str[:-3], '%I:%M %p')
     eastern = pytz.timezone('US/Eastern')
     localized_time = eastern.localize(parsed_time)
     output_time = localized_time.strftime('%H:%M:%S')
     return output_time


def parse_schedule(schedule):
        output = []
        for day in schedule:
            for date, games in day.items():
                supabase_date = convert_date(date)
                # print(f"Date: {supabase_date}")
                for game in games:
                    time, home, opponent = game
                    supabase_time = convert_time(time)
                    home = get_abbreviation(home)
                    opponent = get_abbreviation(opponent)
                    # print(f"  Time: {supabase_time}")
                    # print(f"  Game: {home} vs {opponent}")
                    output.append({
                    "date": supabase_date,
                    "home_team": home,
                    "time": supabase_time,
                    "opponent_team": opponent})
                # print() 
        # print(output)  
        return output

def scrape_schedule():
    # Set up the Chrome options
    options = Options()
    options.headless = True
    # Path to the ChromeDriver executable
    driver_path = '/opt/homebrew/bin/chromedriver'
    s = Service(driver_path)

    driver = webdriver.Chrome(service=s, options=options)
    # print(driver)
    # Open the webpage

    driver.get("https://www.nba.com/schedule")
    wait = WebDriverWait(driver, 10)
    schedule = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.ScheduleDay_sd__GFE_w")))
    game_list = []
    for day in schedule:
        # print("entered loop")
        day_list = []
        date = day.find_element(By.CSS_SELECTOR, "h4.ScheduleDay_sdDay__3s2Xt").text
        games = day.find_elements(By.CSS_SELECTOR, "div.ScheduleGame_sg__RmD9I")
        for game in games:
            time = game.find_element(By.CSS_SELECTOR, "span.ScheduleStatusText_base__Jgvjb").text
            teams = game.find_elements(By.CSS_SELECTOR, "div.ScheduleGame_sgTeam__TEPZa")
            teams = [t.text for t in teams]
            new_game = [time, teams[0], teams[1]]
            day_list.append(new_game)
        game_list.append({date:day_list})
    driver.quit()
    # print(game_list)
    if game_list:
        return parse_schedule(game_list)

    






#return game_list


# def get_schedule():
#     game_list = scrape_schedule()   
#     print(game_list)
#     with open("/Users/hunterzhang/Desktop/scrappersManager/temp.txt", "a") as file:
#                 file.write(f"{game_list} \n")
#     return game_list

# get_schedule()
    
