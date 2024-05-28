from scraper import Scraper

# Example usage
scraper = Scraper()
# pages = ["schedule"]
pages = ["traditional_stats"]
for page in pages:
    result = scraper.get(page)
    print(len(result))
    scraper.upload(page)
scraper.close()
