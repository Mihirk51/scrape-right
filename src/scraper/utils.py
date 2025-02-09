from lxml import html
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
import requests
from datetime import datetime


def get_date_from_xpath(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.content)

    element = tree.xpath('//div[contains(@class, "event-desc-item-value")][1]')

    return element[0].text_content().strip() if element else "Element not found"


def parse_dates(date_string):
    if 'TBD' in date_string:
        return None, None

    if ' - ' in date_string:
        start, end = date_string.split(' - ')
    else:
        start = end = date_string

    # Handle end date first to get the year
    end_parts = end.split(', ')
    if len(end_parts) == 2:  
        end_year = end_parts[1]
        end_month_day = end_parts[0]
    else:  
        start_parts = start.split(', ')
        end_year = start_parts[1] if len(start_parts) > 1 else start.split()[-1]
        end_month_day = end

    # Parse end date
    if ' ' not in end_month_day:  
        end_month = start.split()[0]
        end_str = f"{end_month} {end_month_day}, {end_year}"
    else:
        end_str = f"{end_month_day}, {end_year}"
    end_date = datetime.strptime(end_str, "%b %d, %Y").date()

    # Parse start date
    start_parts = start.split(', ')
    if len(start_parts) == 2:
        start_str = start
    else:
        if ' ' not in start_parts[0]:
            start_month = end_month_day.split()[0]
            start_str = f"{start_month} {start_parts[0]}, {end_year}"
        else:
            start_str = f"{start_parts[0]}, {end_year}"
    start_date = datetime.strptime(start_str, "%b %d, %Y").date()

    if start_date > end_date:
        end_date = end_date + relativedelta(years=1)

    return str(start_date), str(end_date)


def extract_event_details(element):
    name = element.find_element(By.CLASS_NAME, 'event-item-title').text.strip()
    status = element.find_element(By.CLASS_NAME, 'event-item-desc-item-status').text.strip()
    prize_pool = element.find_element(By.CLASS_NAME, 'mod-prize').text.split('\n')[0].strip()
    country = element.find_element(By.TAG_NAME, 'i').get_attribute('class')[-2:]
    logo = element.find_element(By.TAG_NAME, 'img').get_attribute('src')
    href = element.get_attribute('href')
    dates = get_date_from_xpath(href)
    try:
        start_date, end_date = parse_dates(dates)
    except Exception as e:
        print(f"Failed to standardize dates for {dates}: {str(e)}")

    return {
        'name': name,
        'status': status,
        'prize_pool': prize_pool,
        'start_date': start_date,
        'end_date': end_date,
        'country': country,
        'link': href,
        'logo': logo
    }


def extract_page_links(driver, region):
    page_elements = driver.find_element(By.CLASS_NAME, 'action-container-pages')
    page_tags = page_elements.find_elements(By.TAG_NAME, 'a')

    page_links_temp = [pages.get_attribute('href') for pages in page_tags]
    last_page_str = str(page_links_temp[-1][-1])

    return [f"{region}/?page={i}" for i in range(1, int(last_page_str) + 1)]
