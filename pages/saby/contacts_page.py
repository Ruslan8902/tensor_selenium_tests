import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

from ..base_page import BasePage


class ContactsPage(BasePage):
    url = 'https://saby.ru/contacts'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    tensor_banner_locator = (By.CSS_SELECTOR,
                             '#contacts_clients a[title="tensor.ru"]')
    current_region_name_locator = (By.CSS_SELECTOR,
                                   '.sbisru-Contacts__underline .sbis_ru-Region-Chooser__text')
    contacts_items_locator = (By.CSS_SELECTOR,
                              '.sbisru-Contacts-List__item')
    contact_name_locator = (By.CSS_SELECTOR,
                            ".sbisru-Contacts-List__name")
    contact_address_locator = (By.CSS_SELECTOR,
                               ".sbisru-Contacts-List__address .sbisru-Contacts-List--ellipsis")
    cities_items_locator = (By.CSS_SELECTOR,
                            ".sbisru-Contacts-List__city")
    regions_controls_locator = (By.XPATH,
                                '//li[@class="sbis_ru-Region-Panel__item"]')

    # Getters
    @allure.step(f"{url} : Получение элемента баннера Тензор на странице")
    def get_tensor_banner(self):
        ignored_exceptions = (StaleElementReferenceException,)
        return WebDriverWait(self.driver, 30, ignored_exceptions=ignored_exceptions).until(
            EC.element_to_be_clickable(self.tensor_banner_locator))

    @allure.step(f"{url} : Получение элемента кнопки с текущим регионом")
    def get_current_region_name_button(self):
        return WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.current_region_name_locator))

    @allure.step(f"{url} : Получение контактов партнеров")
    def get_contacts_items(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_any_elements_located(self.contacts_items_locator))

    @allure.step("Получение названий городов, в которых есть партнеры")
    def get_cities_items(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_any_elements_located(self.cities_items_locator))

    @allure.step(f"{url} : Получение кнопок с вариантами регионов")
    def get_regions_controls(self):
        return WebDriverWait(self.driver, 30).until(
            EC.visibility_of_all_elements_located(self.regions_controls_locator))

    @allure.step(f"{url} : Получение текста элемента кнопки с текущим регионом")
    def get_current_region_name_text(self):
        return self.get_current_region_name_button().text

    # Actions
    @allure.step(f"{url} : Нажатие на кнопку с текущим регионом")
    def click_current_region_name_button(self):
        self.get_current_region_name_button().click()

    @allure.step(f"{url} : Открытие сайта Tensor нажатием на баннер с названием компании")
    def open_tensor_page_with_banner_link(self):
        self.get_tensor_banner().click()

    # Methods
    def change_current_region_to(self, region_name):
        with allure.step(f"{self.url} : Смена текущего региона на регион с именем '{region_name}'"):
            region_control_locator = self.regions_controls_locator[1] + f'//span[@title="{region_name}"]'
            with allure.step(f"{self.url} : Нажатие на кнопку с текущим регионом"):
                self.click_current_region_name_button()

            with allure.step(f"{self.url} : Нажатие на кнопку с желаемым регионом"):
                control = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, region_control_locator)))
                ActionChains(self.driver).move_to_element(control).click().perform()

            with allure.step(f"{self.url} : Ожидание смены текста кнопки с текущим регионом"):
                ignored_exceptions = (StaleElementReferenceException,)
                WebDriverWait(self.driver, 30, ignored_exceptions=ignored_exceptions).until(
                    EC.text_to_be_present_in_element(self.current_region_name_locator, region_name))

    @allure.step(f"{url} : Получение названия и адреса партнера из элемента контакта партнера")
    def get_contact_info(self, contact_item):
        name = contact_item.find_element(*self.contact_name_locator).text
        address = contact_item.find_element(*self.contact_address_locator).text
        return dict(name=name, address=address)
