import os
import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tools.helpers import every_downloads_chrome

from ..base_page import BasePage


class DownloadPage(BasePage):
    url = 'https://saby.ru/download'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    download_exe_file_link_locator = (By.XPATH,
                                      '//a[contains(@class, "sbis_ru-DownloadNew-loadLink__link")  and contains(text(), "Exe")]')

    @allure.step(f"{url} : Получения элемента с ссылкой для скачивания файла с расширением .exe")
    def get_download_exe_file_link(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.download_exe_file_link_locator))

    @allure.step(f"{url} : Cкачивание файла с расширением .exe")
    def download_installer_exe_file(self):
        with allure.step("Нажатие на ссылку скачивания файла с расширением .exe"):
            self.get_download_exe_file_link().click()
            return WebDriverWait(self.driver, 120, 1).until(every_downloads_chrome)
