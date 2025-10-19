import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..base_page import BasePage


class MainPage(BasePage):
    url = 'https://saby.ru'
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    contacts_button_locator = (By.CSS_SELECTOR, '.sbisru-Header-ContactsMenu__title')
    contacts_more_link_locator = (By.CSS_SELECTOR, '.sbisru-Header-ContactsMenu__items a[href="/contacts"]')
    download_local_versions_link_locator = (By.CSS_SELECTOR,'a[href="/download"]')

    # Getters
    @allure.step(f"{url} : Получение элемента кнопки 'Контакты'")
    def get_contacts_button(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.contacts_button_locator))

    @allure.step(f"{url} : Получение элемента ссылки с дополнительными контактами")
    def get_contacts_more_link(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.contacts_more_link_locator))

    @allure.step(f"{url} : Получение элемента ссылки на страницу скачивания установочных файлов")
    def get_download_local_versions_link(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.download_local_versions_link_locator))


    # Methods
    @allure.step(f"{url} : Переход на страницу с контактам")
    def open_contacts_page(self):
        with allure.step("Нажатие на кнопку 'Контакты'"):
            self.get_contacts_button().click()
        with allure.step("Нажатие на ссылку с дополнительными контактами"):
            self.get_contacts_more_link().click()

    @allure.step(f"{url} : Переход на страницу страницу скачивания установочных файлов")
    def open_download_local_versions_page(self):
        with allure.step("Нажатие на ссылку страниы скачивания установочных файлов"):
            self.get_download_local_versions_link().click()