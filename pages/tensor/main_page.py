import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..base_page import BasePage


class MainPage(BasePage):
    url = "https://tensor.ru"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    index_cards_locator = (By.CSS_SELECTOR, '.tensor_ru-Index__card')
    index_card_title_locator = (By.CSS_SELECTOR, '.tensor_ru-Index__card-title')
    index_card_more_link_locator = (By.CSS_SELECTOR, '.tensor_ru-Index__link')

    # Getters
    @allure.step(f"{url} : Получение информационных блоков")
    def get_index_cards(self):
        return self.driver.find_elements(*self.index_cards_locator)

    # Actions
    def click_more_link_of_index_card_with_title(self, title):
        with allure.step(f"{self.url} : Переход по ссылке подробнее информационного блока"
                         f" с заголовком '{title}'"):
            index_cards = self.get_index_cards()
            index = self.have_index_card_with_title_text(title)
            if index != -1:
                index_cards[index].find_element(*self.index_card_more_link_locator).click()

    # Methods
    def have_index_card_with_title_text(self, title):
        with allure.step(f"{self.url} : Получение индекса информационного блока"
                         f" с заголовком '{title}'"):
            found_index = -1

            WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located(self.index_card_title_locator))
            index_cards = self.get_index_cards()
            for i in range(len(index_cards)):
                if index_cards[i].find_element(*self.index_card_title_locator).text == title:
                    found_index = i
                    break

            return found_index
