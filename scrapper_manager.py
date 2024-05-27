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

def get_schedule():
    import nba_schedule_scrapper
    schedule_output= nba_schedule_scrapper.scrape_schedule()
    print(schedule_output)
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
    return []
    # import player_boxscore_regular_season_scrapper
    # player_boxscore_regular_season_scrapper.get_player_boxscore()
    
schedule.every(10).seconds.do(get_schedule)

while True:
    schedule.run_pending()
    time.sleep(1)


