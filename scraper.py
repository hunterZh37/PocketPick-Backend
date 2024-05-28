import os
import time
import util
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from supabase import create_client, Client 
from selenium.webdriver.common.by import By
from categories.schedule import get_schedule
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from categories.trad_stats import get_traditional_stats
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class Supabase:
    def __init__(self, data = None):
        load_dotenv()
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        try:
            self.supabase = create_client(self.url, self.key)
            print("supabase has been initiated at -> ", self.supabase)
        except Exception as e:
            print(f"An error occurred: {e}")
        self.data = data
        self.header = None
    
    def setData(self, data):
        self.data = data
        if data:
            self.header = list(data[0].keys())

    def insert(self, category, new_data):
        try:
            data = self.supabase.table(category).insert(new_data).execute()
            print("Inserted successfully!")
        except Exception as e:
            print(f"Insert: An error occurred: {e}")
    
    def delete(self, category):
        try:
            data = self.supabase.table(category).delete().neq(self.header[0], "").execute()
            print("Deleted successfully!")
        except Exception as e:
            print(f"Delete: An error occurred: {e}")
    
    def change(self, category):
        json_file = f"json/{category}.json"
        old_data = util.load_previous_file(json_file)
        changes = util.detect_changes(self.data, old_data)
        if changes:
            util.notify_changes(changes)
            self.delete(category)
            util.save_file(self.data, json_file)
            self.insert(category, self.data)
        else:
            print("No changes detected")



class Scraper:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.driver_path = '/opt/homebrew/bin/chromedriver'
        self.s = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=self.s, options=self.options)
        self.supabase = Supabase()
    
    def get(self, category):
        data = None
        if category == "schedule":
            data = get_schedule(self.driver)
        elif category == "traditional_stats":
            data = get_traditional_stats(self.driver)
        else:
            data = None
        self.supabase.setData(data)
        return data

    def upload(self, category):
        self.supabase.change(category)
        
    def close(self):
        self.driver.quit()

        
    
    
    
