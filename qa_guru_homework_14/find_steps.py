import allure
from selene import be, by, have, query

from qa_guru_homework_14.mountain import Mountain


class FindSteps:

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открыть сайт с вершинами и их маршрутами")
    def open(self):
        self.driver.open("https://alpmap.ru/")

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
                dialog.element('button:has-text("Закрыть")').click()

            # Проверяем закрытие
            dialog.should(be.not_.visible)

        except Exception as e:
            print(f"⚠️  Модальное окно не найдено или не закрыто: {e}")
            # Если модалки нет, просто продолжаем тест
            pass

    @allure.step("Найти пики у горы")
    def find_mount_by_name(self, mount: Mountain):

        # Поиск по названию горы
        search_field = self.driver.element(
            '[aria-label="Поиск по названию вершины"]'
        )
        search_field.should(be.visible.and_(be.enabled))
        search_field.type(mount.mount_name)

    @allure.step("Найти маршруты на выбранный пик")
    def find_routes_by_peak_name(self, mount: Mountain):
        # Поиск по названию пика вершины
        peak_element = self.driver.element(
            f'//div[text()="{mount.mount_peak_name}"]'
        )
        peak_element.should(be.visible).click()

    @allure.step("Проверить отображение указателя на пик на карте")
    def check_visible_peak_pointer(self, mount: Mountain):
        # Поиск отображения указателя для пика вершины
        elbrus_marker = self.driver.element(
            f'img[alt="{mount.mount_peak_name}"]'
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
