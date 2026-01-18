import logging

import allure
from selene import be, browser, by, have, query
from selenium.common import TimeoutException

from models.mountain import Mountain


class RouteSteps:

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открыть сайт с вершинами и их маршрутами")
    def open(self, url="https://alpmap.ru/"):
        self.driver.open(url)

    @allure.step("Найти пики у горы")
    def find_mount_by_name(self, mount_name):

        # Поиск по названию горы
        search_field = self.driver.element(
            '[aria-label="Поиск по названию вершины"]'
        )
        search_field.should(be.visible.and_(be.enabled))
        search_field.type(mount_name)

    @allure.step("Найти маршруты на выбранный пик")
    def find_routes_by_peak_name(self, name):
        # Поиск по названию пика вершины
        peak_element = self.driver.element(f'//div[text()="{name}"]')
        peak_element.should(be.visible).click()

    @allure.step("Проверить отображение указателя на пик на карте")
    def check_visible_peak_pointer(self, name):
        # Поиск отображения указателя для пика вершины
        mount_marker = self.driver.element(f'img[alt="{name}"]')
        mount_marker.with_(timeout=10).should(be.visible)

    @allure.step(
        "Проверить соответствие отображаемых маршрутов для выбранного пика"
    )
    def should_have_routes(self, mount: Mountain):
        """Проверяем, что таблица содержит все ожидаемые маршруты"""

        routes_container = self.driver.element("div.flex.flex-col.gap-3")
        routes_container.should(be.visible)

        expected_routes = mount.route_list

        for route_name in expected_routes:
            routes_container.should(have.text(route_name))

    @allure.step("Отфильтровать горы по категории")
    def filter_mount_by_categories(self, category):

        filter_button = browser.all(
            '[id^="headlessui-disclosure-button-"]'
        ).element_by(have.text("Фильтр"))
        filter_button.click()

        checkbox_category = browser.element(f"#capability-{category}")
        checkbox_category.should(be.visible)
        checkbox_category.click()

        browser.all("button").element_by(have.text("Применить")).should(
            be.visible
        ).click()

    @allure.step("Проверить наличие категорий у гор в результате фильтрации")
    def check_mountains_category(self, category):

        title_div = browser.element("div.text-lg.text-gray-600")
        title_div.should(be.visible)
        visible_peaks_container = title_div.element("./..")

        peak_cards = visible_peaks_container.all("button[aria-label]")

        peak_cards_list = peak_cards  # Получаем список элементов

        for peak_card in peak_cards_list:
            # 5А категория сложности
            peak_card.element(by.text(category)).should(be.existing)

    @allure.step("Проверить отсутствие результата фильтрации")
    def check_mount_not_found(self):
        browser.element(
            by.text("Нет вершин подходящих под выбранные фильтры")
        ).should(be.existing)

    @allure.step("Открыть маршрут на сайте ФАР")
    def open_route_in_far(self, route_name):
        title = browser.all("h3").element_by(have.text(f"{route_name}"))
        parent = title.element("./../..")
        far_link = parent.all("a").element_by(have.text("ФАР"))
        far_link.click()

    @allure.step("Проверить корректность открытого маршрута")
    def check_table_values(self, mount_name, route_name, region):
        browser.switch_to_next_tab()

        # table = browser.element(".route-desc__table").should(be.visible, timeout=30)
        # table.should(be.existing)
        # table.element(by.text(route_name)).should(be.existing)
        # table.element(by.text(mount_name)).should(be.existing)
        # table.element(by.text(region)).should(be.existing)

        try:
            table = browser.element(".route-desc__table").should(be.visible, timeout=30)
            table.should(be.existing)
            table.element(by.text(route_name)).should(be.existing)
            table.element(by.text(mount_name)).should(be.existing)
            table.element(by.text(region)).should(be.existing)

        except TimeoutException as e:
            logging.error(f"Timeout waiting for elements: {str(e)}")
            browser.save_screenshot("timeout_error.png")
            raise
        except AssertionError as e:
            logging.error(f"Assertion failed: {str(e)}")
            browser.save_screenshot("assertion_error.png")
            raise