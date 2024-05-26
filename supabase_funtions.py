import time
import os
from supabase import create_client, Client 
import schedule

# ----------------- init -----------------

SUPABASE_URL="https://nnbdlnflutymeudqdaqc.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5uYmRsbmZsdXR5bWV1ZHFkYXFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQwMjI5NjQsImV4cCI6MjAyOTU5ODk2NH0.vYc5COQvFK4QDF_lGpXLHltVRoJEtR1B8T8wUQHHXPc"
# url = os.environ.get("SUPABASE_URL")
# key = os.environ.get("SUPABASE_KEY")
url = SUPABASE_URL
key = SUPABASE_KEY

try:
    supabase = create_client(url, key)
    print("supabase has been initiated at -> ", supabase)
except Exception as e:
    print(f"An error occurred: {e}")
# ----------------- init -----------------

def readData():
    data = supabase.table("temp").select("*").execute()
    print(data)

def insertData():
    try:
        data = supabase.table("temp").insert([{"id":3, "name":"Germany123"},{"id":311, "name":"Germany1212123"}]).execute()
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")

def get_schedule():
    import nba_schedule
    nba_schedule.scrape_schedule()
    insertData()
    
schedule.every(10).seconds.do(get_schedule)

while True:
    schedule.run_pending()
    time.sleep(1)


