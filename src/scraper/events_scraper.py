import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config.settings import BASE_URL, REGIONS, CHROMEDRIVER_PATH, SLEEP_TIME
from logger import logger
from .utils import extract_event_details, extract_page_links

service = Service(executable_path=CHROMEDRIVER_PATH)
events_base_url = f"{BASE_URL}events/"
region_mapping_links = {
    key: f"{events_base_url}{value}"
    for key, value in REGIONS.items()
}


class EventScraper:
    def __init__(self, region):
        self.region = region
        self.driver = webdriver.Chrome(service=service)
        logger.info(f"Initialized EventScraper for region: {region}")

    def get_all_events(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'event-item')
        events = [extract_event_details(element) for element in elements]
        logger.debug(f"Scraped {len(events)} events")
        return events

    def get_all_page_links(self):
        page_links = extract_page_links(self.driver, self.region)
        logger.debug(f"Found {len(page_links)} page links")
        return page_links

    def get_all_events_main(self):
        base_url = f"{self.region}/?page=1"
        self.driver.get(base_url)
        time.sleep(SLEEP_TIME)

        page_links = self.get_all_page_links()

        events = []
        for page in page_links:
            self.driver.get(page)
            time.sleep(SLEEP_TIME)
            events.extend(self.get_all_events())
        self.driver.quit()

        with open('events.json', 'w') as json_file:
            json.dump(events, json_file, indent=4)

        logger.info(f"Scraped and saved {len(events)} events to events.json")
        return events
