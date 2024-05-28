import time
import pytz
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

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

def convert_time(time_str):
     parsed_time= datetime.strptime(time_str[:-3], '%I:%M %p')
     eastern = pytz.timezone('US/Eastern')
     localized_time = eastern.localize(parsed_time)
     output_time = localized_time.strftime('%H:%M:%S')
     return output_time

def parse_schedule(game_list):
    output = []
    for game in game_list:
        date, time, home, opponent = game
        supabase_date = convert_date(date)
        supabase_time = convert_time(time)
        home = get_abbreviation(home)
        opponent = get_abbreviation(opponent)
        output.append({
        "date": supabase_date,
        "home_team": home,
        "time": supabase_time,
        "opponent_team": opponent})

    # for day in game_list:
    #     for date, games in day.items():
    #         supabase_date = convert_date(date)
    #         for game in games:
    #             time, home, opponent = game
    #             supabase_time = convert_time(time)
    #             home = get_abbreviation(home)
    #             opponent = get_abbreviation(opponent)
    #             output.append({
    #             "date": supabase_date,
    #             "home_team": home,
    #             "time": supabase_time,
    #             "opponent_team": opponent})
    return output

def get_schedule(driver):
        driver.get("https://www.nba.com/schedule")
        time.sleep(5)
        driver.minimize_window()
        schedule = driver.find_elements(By.CSS_SELECTOR, "div.ScheduleDay_sd__GFE_w")
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
        if game_list:
             return parse_schedule(game_list)
        else:
            return None
        # df = pd.DataFrame(game_list, columns=header)
        # return df