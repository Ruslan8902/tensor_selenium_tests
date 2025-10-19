import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os

@pytest.fixture(scope="function")
def browser(request):
    options_chrome = Options()

    prefs = {
        "download.default_directory": os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/tests/download"),
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True,
        }
    options_chrome.add_experimental_option("prefs", prefs)
    options_chrome.add_argument('--headless=new')
    options_chrome.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=options_chrome)
    browser.maximize_window()
    yield browser
    browser.quit()