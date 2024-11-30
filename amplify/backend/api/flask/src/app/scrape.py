from app import util
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, JavascriptException
from dataclasses import dataclass, field
import subprocess
import re


@dataclass
class SiteInfo():
    name: str = ''
    description: str = ''
    offerings: list[str] = field(default_factory=list)


@dataclass
class ScrapeResults(SiteInfo):
    success: bool = True
    status: int = 200

    def __str__(self):
        return f'{self.name}: {self.description} Offerings: {self.offerings}'


def get_data(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-crash-reporter')
    options.add_argument('--start-maximized')
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
    driver.set_page_load_timeout(30)

    try:
        driver.get(url)
    except TimeoutException:
        return ScrapeResults(
            description='Error: Page load timed out',
            success=False,
            status=504
        )

    ensure_page_loaded(driver)
    page_links = gather_links(driver)
    site_name = find_name(driver, url)
    site_desc = find_desc(driver, page_links)
    site_offerings = find_offerings(driver, page_links)

    driver.quit()

    if site_name == 'Just a moment...':
        return ScrapeResults(
            name=util.name_from_url(url),
            description='Error: Blocked by site security (Cloudflare)',
            success=False,
            status=500
        )

    return ScrapeResults(site_name, site_desc, site_offerings)


def ensure_page_loaded(driver):
    await_script_condition(driver, 'jQuery.active == 0')
    await_script_condition(driver, 'angular.element(document).injector().get("$http").pendingRequests.length) === 0')


def await_script_condition(driver, script):
    wait = WebDriverWait(driver, timeout=1.5, poll_frequency=0.3)

    try:
        wait.until(lambda d: driver.execute_script(f'return {script}'))
    except (JavascriptException, TimeoutException):
        pass


def gather_links(driver):
    try:
        return driver.find_elements(By.TAG_NAME, 'a')
    except NoSuchElementException:
        return []


def find_name(driver, url):
    name = ''
    try:
        title = driver.find_element(By.TAG_NAME, 'title')
        name = title.get_attribute('innerText')
    except NoSuchElementException:
        pass

    if len(name) == 0:
        name = util.name_from_url(url)

    return name


def find_desc(driver, page_links):
    try:
        el = driver.find_element(By.CSS_SELECTOR, 'meta[name="description"], meta[name="Description"]')
        desc = el.get_attribute('content')
    except NoSuchElementException:
        desc = ''

    if len(desc) == 0:
        desc = desc_from_about(driver, page_links)

    return desc


def desc_from_about(driver, page_links):
    try:
        about_link = next('About' in a.get_attribute('innerText') for a in page_links)
        driver.get(about_link.get_attribute('href'))
        first_title = driver.find_element(By.CSS_SELECTOR, 'h1, h2, h3, h4, h5, h6')
    except (StopIteration, NoSuchElementException, TimeoutException):
        return ''

    return first_title.get_attribute('innerText')


def find_offerings(driver, page_links):
    regexp = re.compile(r'(Products)|(Services)|(Solutions)|(Store)', re.IGNORECASE)
    not_selectors = ':not(header *):not(nav *):not(aside *):not([class*="breadcrumb"])'

    try:
        offerings_link = next(a for a in page_links if regexp.match(get_text(a)))
        driver.get(offerings_link.get_attribute('href'))
        offering_list = driver.find_element(By.CSS_SELECTOR, f'ul:not([role=listbox]){not_selectors}, [role="list"]{not_selectors}')
    except (StopIteration, NoSuchElementException, TimeoutException):
        return []

    children = offering_list.find_elements(By.CSS_SELECTOR, '*')
    child_text = list(set(get_text(c) for c in children))
    return [el for el in child_text if el != '']


def get_text(element):
    return element.get_attribute('innerText').strip(' \t\r\n')
