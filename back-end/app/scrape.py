import re
import subprocess
from typing import NamedTuple
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, JavascriptException


class ScrapeResults(NamedTuple):
    name: str
    description: str
    text: list[str]


def get_data(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument("--disable-crash-reporter")
    options.experimental_options['prefs'] = {
        'profile.default_content_settings': {
            'images': 2,
            'cookies': 2,
            'plugins': 2,
            'popups': 2,
            'geolocation': 2,
            'notifications': 2,
            'media_stream': 2
        }
    }

    service = Service(service_args=['--log-level=WARNING'], log_output=subprocess.STDOUT)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    site_name = find_name(driver, url)
    site_desc = find_desc(driver)
    text_segments = scrape_text(driver)

    driver.quit()

    return ScrapeResults(site_name, site_desc, text_segments)


def scrape_text(driver):
    text_element_selector = 'h1, h2, h3, h4, h5, h6, p, li, dt, dd, th, td, a, pre, span'
    text_elements = driver.find_elements(By.CSS_SELECTOR, text_element_selector)

    text_segments = []
    for e in text_elements:
        if len(e.text) != 0:
            text_segments.append(e.text)

    return text_segments


def find_name(driver, url):
    name = ''
    try:
        title = driver.find_element(By.TAG_NAME, 'title')
        name = title.get_attribute('innerText')
    except NoSuchElementException:
        pass

    if len(name) == 0:
        name = name_from_url(url)

    return name


def find_desc(driver):
    try:
        el = driver.find_element(By.CSS_SELECTOR, 'meta[name="description"]')
        desc = el.get_attribute('content')
    except NoSuchElementException:
        desc = ''

    return desc


def name_from_url(url):
    matches = re.findall(r'[\w\d]+\.', url)
    if not matches:
        return ''

    name = matches[-1][:-1]
    return name
