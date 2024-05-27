import time
import os
from supabase import create_client, Client 
import schedule
import utility

# ----------------- init -----------------

SUPABASE_URL="https://nnbdlnflutymeudqdaqc.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5uYmRsbmZsdXR5bWV1ZHFkYXFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQwMjI5NjQsImV4cCI6MjAyOTU5ODk2NH0.vYc5COQvFK4QDF_lGpXLHltVRoJEtR1B8T8wUQHHXPc"
url = SUPABASE_URL
key = SUPABASE_KEY

try:
    supabase = create_client(url, key)
    print("supabase has been initiated at -> ", supabase)
except Exception as e:
    print(f"An error occurred: {e}")
# ----------------- init -----------------

# def readData():
#     data = supabase.table("temp").select("*").execute()
#     print(data)

def insert_schedule_data(schedule_data):
    try:
        data = supabase.table("schedule").insert(schedule_data).execute()
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_schedule_data():
    try:
        data = supabase.table("schedule").delete().neq('home_team', "sdfes").execute()
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")

def insert_player_boxscore_data(player_boxscore_data):
    try:
        data = supabase.table("player_boxscore").insert(player_boxscore_data).execute()
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_player_boxscore_data():
    try:
        data = supabase.table("player_boxscore").delete().neq('name', "sdfes").execute()
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")

def get_schedule():
    import nba_schedule_scraper
    schedule_output = nba_schedule_scraper.scrape_schedule()
    # print(schedule_output)
    old_shedule = utility.load_previous_file("nba_schedule.json")
    changes = utility.detect_changes(schedule_output, old_shedule)

    if changes:
        utility.notify_changes(changes)
        delete_schedule_data()
        utility.save_file(schedule_output, "nba_schedule.json") 
        insert_schedule_data(schedule_output)
    else:
        print("No changes detected")

def get_player_boxscore():
    import player_boxscore_regular_season_scraper
    player_boxscore_output = player_boxscore_regular_season_scraper.scrape_player_boxscore()
    # print(player_boxscore_output)
    old_boxscore = utility.load_previous_file("player_boxscore_regular_season.json")
    changes = utility.detect_changes(player_boxscore_output, old_boxscore)
    # print(changes)

    if changes:
        utility.notify_changes(changes)
        # delete_schedule_data()
        utility.save_file(player_boxscore_output, "player_boxscore_regular_season.json") 
        # insert_schedule_data(player_boxscore_output)
    else:
        print("No changes detected")

    # import player_boxscore_regular_season_scrapper
    # player_boxscore_regular_season_scrapper.get_player_boxscore()
    
# schedule.every(10).seconds.do(get_schedule)
schedule.every(10).seconds.do(get_player_boxscore)

while True:
    schedule.run_pending()
    time.sleep(1)

