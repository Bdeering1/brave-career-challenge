import re
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def scrape(url):
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
        }
    }

    service = Service(service_args=['--log-level=INFO'], log_output=subprocess.STDOUT)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    site_name = find_site_name(driver, url)
    text_segments = scrape_text(driver)

    driver.quit()

    return site_name, text_segments


def scrape_text(driver):
    text_element_selector = 'h1, h2, h3, h4, h5, h6, p, li, dt, dd, th, td, a, pre, span'
    text_elements = driver.find_elements(By.CSS_SELECTOR, text_element_selector)

    text_segments = []
    for e in text_elements:
        if len(e.text) != 0:
            text_segments.append(e.text)

    return text_segments


def find_site_name(driver, url):
    name = ''
    try:
        title = driver.find_element(By.TAG_NAME, 'title')
        name = title.get_attribute('innerHTML')
    except NoSuchElementException:
        pass

    if len(name) == 0:
        name = name_from_url(url)

    return name


def name_from_url(url):
    matches = re.findall(r'[\w\d]+\.', url)
    if not matches:
        return ''

    name = matches[-1][:-1]
    return name
