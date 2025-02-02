from scraper.events_scraper import EventScraper
from config.settings import region_mapping_links

def main():
    region = region_mapping_links['ap']
    scraper = EventScraper()
    events = scraper.get_all_events_main(region)
    for event in events:
        print(event)

if __name__ == "__main__":
    main()