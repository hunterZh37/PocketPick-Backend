import requests
import json
from datetime import datetime

def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" 
    response = requests.get(url)
    data = json.loads (response.text)
    return data['bitcoin']['usd']

def main():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    bitcoin_price = get_bitcoin_price()
    print (f"{current_time} - Bitcoin price: ${bitcoin_price}")
    with open("/Users/hunterzhang/Desktop/scrappersManager/temp.txt", "a") as file: 
        file.write(f"{current_time} - Bitcoin price: ${bitcoin_price}\n")

main()
