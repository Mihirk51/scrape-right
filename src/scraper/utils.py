from selenium.webdriver.common.by import By


def extract_event_details(element):
    name = element.find_element(By.CLASS_NAME, 'event-item-title').text.strip()
    status = element.find_element(By.CLASS_NAME, 'event-item-desc-item-status').text.strip()
    prize_pool = element.find_element(By.CLASS_NAME, 'mod-prize').text.split('\n')[0].strip()
    dates = element.find_element(By.CLASS_NAME, 'mod-dates').text.split('\n')[0].strip()
    country = element.find_element(By.TAG_NAME, 'i').get_attribute('class')[-2:]
    logo = element.find_element(By.TAG_NAME, 'img').get_attribute('src')
    href = element.get_attribute('href')

    return {
        'name': name,
        'status': status,
        'prize_pool': prize_pool,
        'dates': dates,
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