import time

import allure
from selene import be, by, have, query, browser
from selene.core.command import js
from selenium.webdriver.common.by import By

from qa_guru_homework_14.category import Category
from qa_guru_homework_14.mountain import Mountain


class FindSteps:

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открыть сайт с вершинами и их маршрутами")
    def open(self, url="https://alpmap.ru/"):
        self.driver.open(url)

    @allure.step("Закрыть приветственную модалку")
    def close_welcome_modal(self):
        try:
            # Ждем портал с модалкой
            modal_portal = self.driver.element("#headlessui-portal-root")
            modal_portal.with_(timeout=15).should(be.visible)

            # Ищем диалог внутри портала
            dialog = modal_portal.element('[role="dialog"]')
            dialog.should(be.visible)

            # Ищем кнопку разными способами
            close_button = dialog.element("button")

            # Проверяем, что это нужная кнопка (по тексту или другим атрибутам)
            if close_button.get(query.text) == "Закрыть":
                close_button.click()
            else:
                # Если первая кнопка не "Закрыть", ищем по тексту
                dialog.element(by.text("Закрыть")).click()

            # Проверяем закрытие
            dialog.should(be.not_.visible)

        except Exception as e:
            print(f"⚠️  Модальное окно не найдено или не закрыто: {e}")
            # Если модалки нет, просто продолжаем тест
            pass

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
        peak_element = self.driver.element(
            f'//div[text()="{name}"]'
        )
        peak_element.should(be.visible).click()

    @allure.step("Проверить отображение указателя на пик на карте")
    def check_visible_peak_pointer(self, name):
        # Поиск отображения указателя для пика вершины
        elbrus_marker = self.driver.element(
            f'img[alt="{name}"]'
        )
        elbrus_marker.with_(timeout=10).should(be.visible)

    @allure.step(
        "Проверить соответствие отображаемых маршрутов для выбранного пика"
    )
    def should_have_routes(self, mount: Mountain):
        """Проверяем, что таблица содержит все ожидаемые маршруты"""

        # Находим таблицу или контейнер с маршрутами
        routes_container = self.driver.element("div.flex.flex-col.gap-3")
        routes_container.should(be.visible)

        # Ожидаемые названия маршрутов
        expected_routes = mount.route_list

        # Проверяем каждый маршрут
        for route_name in expected_routes:
            routes_container.should(have.text(route_name))

    @allure.step("Отфильтровать горы по категории")
    def filter_mount_by_categories(self, category: Category):

        # Раскрыть фильтр
        filter_button = browser.all('[id^="headlessui-disclosure-button-"]').element_by(have.text('Фильтр'))
        filter_button.click()

        # Выбрать нужные чек-боксы
        checkbox_category = browser.element(f'#capability-{category.category}')
        checkbox_category.should(be.visible)
        checkbox_category.click()

        # Применить фильтр
        browser.all('button').element_by(have.text('Применить')).should(be.visible).click()

    @allure.step("Проверить наличие категорий у гор в результате фильтрации")
    def check_mountains_category(self, category: Category):
        """Проверить, что все видимые вершины содержат категорию 5А"""

        # Найти контейнер видимых вершин
        #visible_peaks_container = (browser.element('div:has-text("Видимые вершины:")').should(be.visible).find('..'))
        title_div = browser.element('div.text-lg.text-gray-600')
        title_div.should(be.visible)
        visible_peaks_container = title_div.element('./..')
        # Найти все карточки вершин внутри контейнера
        peak_cards = visible_peaks_container.all('button[aria-label]')

        peak_cards_list = peak_cards  # Получаем список элементов
        peak_count = len(peak_cards_list)

        # print('ghgjghjggj', visible_peaks_container)
        print(f"Найдено видимых вершин: {peak_count}")

        # Проверить каждую вершину на наличие 5А
        for peak_card in peak_cards_list:
            # 5А категория сложности
            peak_card.element(by.text(category.category)).should(be.existing)

    @allure.step("Проверить отсутствие результата фильтрации")
    def check_mount_not_found(self):
        browser.element(by.text('Нет вершин подходящих под выбранные фильтры')).should(be.existing)

    @allure.step("Открыть маршрут на сайте ФАР")
    def open_route_in_far(self, route_name):
        title = browser.all('h3').element_by(have.text(f"{route_name}"))
        parent = title.element('./../..')
        far_link = parent.all('a').element_by(have.text("ФАР"))
        far_link.click()

    @allure.step("Проверить корректность открытого маршрута")
    def check_table_values(self, mount_name, route_name):
        browser.switch_to_next_tab()

        table = browser.element('.route-desc__table')
        table.should(be.existing)
        table.element(by.text(route_name)).should(be.existing)
        table.element(by.text(mount_name)).should(be.existing)

    @allure.step("Открыть контакты из телеграм")
    def open_telegram_contact(self):
        filter_button = browser.all('[id^="headlessui-disclosure-button-"]').element_by(have.text('Полезные ссылки'))
        filter_button.click()

        link = browser.all(".flex-1.min-w-0").element_by(have.text('Написать автору'))

        # 2. Проверить
        link.should(be.visible)
        link.click()


    @allure.step("Проверить, что открыты нужные контакты из телеграм")
    def check_telegram_contact(self):
        browser.switch_to_next_tab()
        current_url = browser.driver.current_url
        valid_patterns = [
            "https://t.me/alpmap",
            "https://t.me/alpmap/",
            "http://t.me/alpmap",
            "t.me/alpmap",
            "t.me/alpmap/"
        ]

        # Проверить все варианты
        url_is_valid = False
        for pattern in valid_patterns:
            if pattern in current_url:
                url_is_valid = True
                print(f"✓ Найден паттерн: {pattern}")
                allure.attach(f"Соответствует: {pattern}", name="Успех")
                break

        if not url_is_valid:
            # Проверить частично
            if "t.me" in current_url and "alpmap" in current_url:
                print(f"⚠ Частичное совпадение: {current_url}")
                allure.attach(f"Частичное совпадение: {current_url}", name="Предупреждение")
                url_is_valid = True

        if url_is_valid:
            print(f"✓ Telegram контакт проверен: {current_url}")
            return True
        else:
            error_msg = f"URL не соответствует Telegram. Получено: {current_url}"
            allure.attach(f"✗ {error_msg}", name="Ошибка")
            raise AssertionError(error_msg)