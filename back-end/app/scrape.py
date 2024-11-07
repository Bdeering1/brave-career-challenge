import re
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, JavascriptException


class ScrapeResults():
    name: str
    description: str
    success = True
    status = 200

    def __init__(self, name='', description='', success=True, status=200):
        self.name = name
        self.description = description
        self.success = success
        self.status = status

    def __str__(self):
        return f'{self.name}: {self.description}'


def get_data(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-crash-reporter')
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

    try:
        driver.set_page_load_timeout(10)
        driver.get(url)
    except TimeoutException:
        return ScrapeResults(
            description='Error: Page load timed out',
            success=False,
            status=504
        )

    ensure_page_loaded(driver)
    site_name = find_name(driver, url)
    site_desc = find_desc(driver)

    driver.quit()

    if site_name == 'Just a moment...':
        return ScrapeResults(
            description='Error: Blocked by site security (Cloudflare)',
            success=False,
            status=500
        )

    return ScrapeResults(site_name, site_desc)


def ensure_page_loaded(driver):
    await_script_condition(driver, 'jQuery.active == 0')
    await_script_condition(driver, 'angular.element(document).injector().get("$http").pendingRequests.length) === 0')


def await_script_condition(driver, script):
    wait = WebDriverWait(driver, timeout=1.5, poll_frequency=0.3)

    try:
        wait.until(lambda d: driver.execute_script(f'return {script}'))
    except (JavascriptException, TimeoutException):
        pass


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
