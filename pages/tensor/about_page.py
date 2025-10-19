import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..base_page import BasePage


class AboutPage(BasePage):
    url = "https://tensor.ru/about"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    working_section_locator = (By.XPATH,
                               '//div[contains(@class, "tensor_ru-container")]//h2[text()="Работаем"]/parent::div/parent::div')
    imgs_locator = (By.CSS_SELECTOR, 'img')

    # Getters
    @allure.step(f"{url} : Получение блока с заголовком 'Работаем'")
    def get_working_section(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.working_section_locator))

    @allure.step(f"{url} : Получение изображений блока с заголовком 'Работаем'")
    def get_working_section_imgs(self):
        return self.get_working_section().find_elements(*self.imgs_locator)

    @allure.step(f"{url} : Получение уникальных размеров изображений "
                 f"блока с заголовком 'Работаем'")
    def get_working_section_imgs_sizes_sets(self):
        working_section_imgs = self.get_working_section_imgs()
        imgs_width_set = set()
        imgs_height_set = set()

        for img in working_section_imgs:
            imgs_width_set.add(img.size['width'])
            imgs_height_set.add(img.size['height'])

        return dict(
            width_set=imgs_width_set,
            height_set=imgs_height_set
        )
