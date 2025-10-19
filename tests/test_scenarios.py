import allure
import pytest
from selenium.common import TimeoutException

from pages.saby.main_page import MainPage as SabyMainPage
from pages.saby.contacts_page import ContactsPage as SabyContactsPage
from pages.saby.downolad_page import DownloadPage as SabyDownloadPage

from pages.tensor.main_page import MainPage as TensorMainPage
from pages.tensor.about_page import AboutPage as TensorAboutPage
from tools.helpers import get_file_size_in_mb


@allure.story("Проверка успешного получения информации "
              "о компании Tensor через сайт saby.ru")
@allure.tag("Positive")
def test_scenario_1(browser):
    SabyMainPage(browser).open_page()
    SabyMainPage(browser).open_contacts_page()
    SabyContactsPage(browser).open_tensor_page_with_banner_link()

    with allure.step("Переход на новую вкладку браузера"):
        browser.switch_to.window(browser.window_handles[1])

    with allure.step("Проверка наличия блока с заголовком 'Сила в людях'"):
        block_with_title_index = TensorMainPage(browser).have_index_card_with_title_text("Сила в людях")
        assert block_with_title_index != -1, "Нет блока с заголовком 'Сила в людях'"

    with allure.step("Проверка удачного перехода по ссылке 'Подробнее' в блоке 'Сила в людях'"):
        TensorMainPage(browser).click_more_link_of_index_card_with_title("Сила в людях")
        assert browser.current_url == TensorAboutPage(browser).url, \
            f"Ожидалось, что будет открыта страница '{TensorAboutPage(browser).url}'"

    with allure.step("Проверка того, что изображения в блоке 'Работаем' имеет одинаковый размер"):
        working_section_imgs_sizes = TensorAboutPage(browser).get_working_section_imgs_sizes_sets()
        assert len(working_section_imgs_sizes["width_set"]) == 1 \
               and len(working_section_imgs_sizes["height_set"]) == 1


@allure.story("Проверка успешно смены региона "
              "в разделе контактов сайта saby.ru")
@allure.tag("Positive")
@pytest.mark.flaky(retries=2, only_on=[TimeoutException])
def test_scenario_2(browser):
    change_to_region_info = dict(
        name="Камчатский край",
        url="https://saby.ru/contacts/41-kamchatskij-kraj?tab=clients",
        cities=[
            dict(
                city_name="Петропавловск-Камчатский",
                contacts=[
                    dict(
                        name="Saby - Камчатка",
                        address="пр-кт Карла Маркса, д. 31/2, оф. 315"
                    )
                ]
            )
        ]
    )

    SabyContactsPage(browser).open_page()
    with allure.step("Проверка того, что текущий регион == 'Челябинская обл.'"):
        current_region = SabyContactsPage(browser).get_current_region_name_text()
        assert current_region == "Челябинская обл.", f'Ожидалось "Челябинская обл.", получено {current_region}'

    with allure.step("Проверка наличия контактов партнеров на странице"):
        contacts_items = SabyContactsPage(browser).get_contacts_items()
        assert len(contacts_items) > 0, f"Нет контактов партнеров"

    with allure.step("Проверка удачной смены региона"):
        SabyContactsPage(browser).change_current_region_to(change_to_region_info["name"])
        current_region = SabyContactsPage(browser).get_current_region_name_text()
        assert current_region == change_to_region_info["name"], \
            f'Ожидалось "{change_to_region_info["name"]}" получено {current_region}'
        assert browser.current_url == change_to_region_info["url"], \
            f'Ожидался url {change_to_region_info["url"]}, получен url {browser.current_url} '
        assert change_to_region_info["name"] in browser.title, f'В title страницы нет {change_to_region_info["name"]}'

    with allure.step("Проверка того, что на странице указаны все требуемые города"):
        cities = SabyContactsPage(browser).get_cities_items()
        assert len(cities) == len(change_to_region_info["cities"])

    with allure.step("Проверка того, что на странице верно указан первый город"):
        expected_city_name = change_to_region_info["cities"][0]["city_name"]
        assert cities[0].text == expected_city_name, \
            f'Ожидалось "{expected_city_name}", получен "{cities[0].text}"'

    with allure.step("Проверка того, что на странице указано верное количество партнеров"):
        contacts_items = SabyContactsPage(browser).get_contacts_items()
        assert len(contacts_items) == sum([len(city["contacts"]) for city in change_to_region_info["cities"]])

    with allure.step("Проверка того, что на странице указаны верные данные первого партнера"):
        contact_info = SabyContactsPage(browser).get_contact_info(contacts_items[0])
        expected_name = change_to_region_info["cities"][0]["contacts"][0]["name"]
        expected_address = change_to_region_info["cities"][0]["contacts"][0]["address"]
        assert contact_info["name"] == expected_name, \
            f'Ожидалось "{expected_name}", получен "{contact_info["name"]}"'
        assert contact_info["address"] == expected_address, \
            f'Ожидалось "{expected_address}", получен "{contact_info["address"]}"'


@allure.story("Проверка успешного скачивания веб-установщика")
@allure.tag("Positive")
def test_scenario_3(browser):
    SabyMainPage(browser).open_page()
    SabyMainPage(browser).open_download_local_versions_page()

    with allure.step("Проверка удачного скачивания файла по ссылке"):
        path = SabyDownloadPage(browser).download_installer_exe_file()[0]
        assert path.endswith(".exe") and "saby-setup" in path, "Файл не скачан"

    with allure.step("Проверка размера скачанного файла"):
        expected_file_size = 6.35
        file_size = round(get_file_size_in_mb(path), 2)
        assert file_size == expected_file_size, \
            (f"Ожидаемы размер файла {expected_file_size},"
             f"а размер скачанного файла {file_size} ")
