import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config.settings import BASE_URL, REGIONS, CHROMEDRIVER_PATH
from logger import logger  # Import the logger

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
        events = []
        for element in elements:
            name = element.find_element(By.CLASS_NAME, 'event-item-title').text.strip()
            status = element.find_element(By.CLASS_NAME, 'event-item-desc-item-status').text.strip()
            prize_pool = element.find_element(By.CLASS_NAME, 'mod-prize').text.split('\n')[0].strip()
            dates = element.find_element(By.CLASS_NAME, 'mod-dates').text.split('\n')[0].strip()
            country = element.find_element(By.TAG_NAME, 'i').get_attribute('class')[-2:]
            logo = element.find_element(By.TAG_NAME, 'img').get_attribute('src')
            href = element.get_attribute('href')

            event = {
                'name': name,
                'status': status,
                'prize_pool': prize_pool,
                'dates': dates,
                'country': country,
                'link': href,
                'logo': logo
            }
            events.append(event)

        logger.debug(f"Scraped {len(events)} events")
        return events

    def get_all_page_links(self):
        page_elements = self.driver.find_element(By.CLASS_NAME, 'action-container-pages')
        page_tags = page_elements.find_elements(By.TAG_NAME, 'a')

        page_links_temp = [pages.get_attribute('href') for pages in page_tags]
        last_page_str = str(page_links_temp[-1][-1])

        page_links = [f"{self.region}/?page={i}" for i in range(1, int(last_page_str) + 1)]

        logger.debug(f"Found {len(page_links)} page links")
        return page_links

    def get_all_events_main(self):
        base_url = f"{self.region}/?page=1"
        self.driver.get(base_url)
        time.sleep(1)

        page_links = self.get_all_page_links()

        events = []
        for page in page_links:
            self.driver.get(page)
            time.sleep(1)
            events.extend(self.get_all_events())
        self.driver.quit()

        with open('events.json', 'w') as json_file:
            json.dump(events, json_file, indent=4)

        logger.info(f"Scraped and saved {len(events)} events to events.json")
        return events
